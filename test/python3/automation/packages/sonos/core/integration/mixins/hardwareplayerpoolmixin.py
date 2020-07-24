
import traceback

import requests

from akit.exceptions import AKitConfigurationError, AKitInitialConnectivityError, AKitMissingResourceError

from akit.integration.agents.upnpagent import UpnpAgent
from akit.mixins.integration import IntegrationMixIn
from akit.networking.interfaces import get_correspondance_interface
from akit.xformatting import indent_lines

class HardwarePlayerPoolMixin(IntegrationMixIn):

    reference_ip = None
    refernece_port = None

    correspondance_interface = None

    upnp_agent = None

    expected_device_table = None

    def __init__(self, upnp_device, *args, role=None, **kwargs):
        self._upnp_device = upnp_device
        super(HardwarePlayerPoolMixin, self).__init__(*args, role=role, **kwargs)
        return

    @classmethod
    def attach_to_environment(cls):
        """
            This API is called on the HardwarePlayerPoolMixin so it can process configuration information.  The 
            :class:`HardwarePlayerPoolMixin` can then verify that it has a valid environment and configuration
            to run in.

            :raises :class:`akit.exceptions.AKitMissingConfigError`, :class:`akit.exceptions.AKitInvalidConfigError`:
        """   
        super(HardwarePlayerPoolMixin, cls).attach_to_environment()

        # IMPORTANT: This check is important to prevent noisy test runs and failures due to configuration errors.
        if "pod" not in cls.landscape._landscape_info:
            errmsg = "ERROR: In order to attach to an environment when a Hardware Player Pool" \
                " is involved, there must be an 'pod' declaration in the landscape.json config file."
            raise AKitConfigurationError(errmsg)

        pod_info = cls.landscape._landscape_info["pod"]

        # IMPORTANT: This check is important to prevent noisy test runs and failures due to configuration errors.
        if "reference" not in pod_info or 'ip' not in pod_info["reference"] or 'port' not in pod_info["reference"]:
            errmsg = "ERROR: In order to ensure we can communicate on the correct network with the 'pod' devices, " \
                "the 'pod' must contain 'reference' item that contains both an 'ip' and 'port'."
            raise AKitConfigurationError(errmsg)

        ref_info = pod_info["reference"]
        cls.reference_ip = ref_info["ip"]
        cls.reference_port = int(ref_info["port"])

        cls.correspondance_interface, _ = get_correspondance_interface(cls.reference_ip, cls.reference_port)

        return

    @classmethod
    def collect_resources(cls):
        """
            This API is called so the `IntegrationMixIn` can connect with a resource management
            system and gain access to the resources required for the automation run.

            :raises :class:`akit.exceptions.AKitResourceError`:
        """
        # NOTE: This is important to implemented in the case of resources shared at a enterprise level.  The
        # hardware player pool has a listing of expected resources dedicated for it to manage and the automation pod
        # will only ever run one job at a time so we do not need to checkout resources from an enterprise resource
        # manager.  This would be used in the case of some sort of virtual resource pool where resources are obtained
        # on the fly by the automation framework.
        return

    @classmethod
    def diagnostic(cls, diag_level, diag_folder):
        """
            The API is called by the :class:`akit.sequencer.Sequencer` object when the automation sequencer is 
            building out a diagnostic package at a diagnostic point in the automation sequence.  Example diagnostic
            points are:

            * pre-run
            * post-run

            Each diagnostic package has its own storage location so derived :class:`akit.scope.ScopeMixIn` objects
            can simply write to their specified output folder.

            :param diag_level: The maximum diagnostic level to run dianostics for.
            :type diag_level: int
            :param diag_folder: The output folder path where the diagnostic information should be written.
            :type diag_folder: str
        """
        return

    @classmethod
    def establish_connectivity(cls):
        """
            This API is called so the `IntegrationMixIn` can establish connectivity with any compute or storage
            resources.

            :raises :class:`akit.exceptins.AKitInitialConnectivityError`:
        """

        upnp_agent = UpnpAgent(interface=cls.correspondance_interface)
        cls.upnp_agent = upnp_agent

        upnp_agent.start()
        upnp_agent.begin_search()

        upnp_hint_list = cls.landscape.get_upnp_devices()

        # IMPORTANT: We need to make sure all the devices have been found by the UpnpAgent before we continue
        # the setup of the automation run.
        upnp_agent.wait_for_devices(upnp_hint_list)

        found_msg = "==================== DEVICES FOUND ====================\n"
        for device in upnp_agent.children:
            devstr = str(device)
            found_msg += devstr
        found_msg += "\n\n"
        
        cls.logger.info(found_msg)

        # Go through all the devices found and pull out references to all the devices
        # that are in the expected list.  These are the devices we want to work with
        # in automation
        expected_devices_found = []
        expected_devices_missing = [dev for dev in upnp_hint_list]
        for device in upnp_agent.children:
            devmac = device.MACAddress
            if devmac in expected_devices_missing:
                expected_devices_found.append(device)
                expected_devices_missing.remove(devmac)

        # IMPORTANT: Make sure there were no expected devices missing and fail loudly if there were
        if len(expected_devices_missing) > 0:
            # If we got here, then there are devices missing from the testbed that were
            # expected to be there.  We should not continue the automation run
            missingmsg = "ERROR: The following devices were missing:\n"
            for devmac in expected_devices_missing:
                missingmsg += "    %s\n" % devmac
            raise AKitMissingResourceError(missingmsg)

        cls.logger.info("All expected devices were found.")
        
        cls.expected_device_table = {}
        for device in expected_devices_found:
            devmac = device.MACAddress
            cls.expected_device_table[devmac] = device
        
        # IMPORTANT: Make sure we have the minimum automation connectivity with each device
        failing_devices = HardwarePlayerPoolMixin.verify_expected_device_table_connectivity(cls.expected_device_table)
        if len(failing_devices) > 0:
            # If there were devices that failed to have the minimum amount of connectivity\
            # then we need to fail loudly here.
            conn_err_msg = "ERROR: Device connectivity issues were encountered:\n"

            for device, failurereport in failing_devices:
                dev_msg += "    DEVICE: %s\n" % device
                dev_msg += indent_lines(failurereport, 2)
                conn_err_msg += "%s\n" % dev_msg

            raise AKitInitialConnectivityError(conn_err_msg)

        return

    @staticmethod
    def verify_device_connectivity(device):
        
        devip = device.IPAddress

        # Verify connectivity to port 1400 for plain HTTP requests
        statusurl = "http://%s:1400/status"
        req = requests.Request(statusurl)

        # Verify connectivity to port 1440 for secure HTTP requests, this can fail
        # if the R_TRUST_SONOS_DEV_CERT_BIT DevMode bit is not set 

        # Verify connectivity to the telnet port, this can fail if
        # the player has not been telnet unlocked

        return

    @staticmethod
    def verify_expected_device_table_connectivity(expected_device_table):
        
        failing_devices = {}

        for device in expected_device_table.values():
            try:
                HardwarePlayerPoolMixin.verify_device_connectivity(device)
            except Exception:
                failurereport = traceback.format_exc()
                devmac = device.MACAddress
                failing_devices[devmac] = (device, failurereport)

        return failing_devices