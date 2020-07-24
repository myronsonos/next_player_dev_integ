

import traceback

import requests

from akit.exceptions import AKitConfigurationError, AKitInitialConnectivityError, AKitMissingResourceError

from akit.integration.landscaping import LandscapeDescription
from akit.integration.landscaping import Landscape
from akit.integration.agents.upnpagent import UpnpAgent

from akit.networking.interfaces import get_correspondance_interface

from akit.xformatting import indent_lines

class SonosLandscapeDescription(LandscapeDescription):
    """
    """

    @classmethod
    def register_integration_points(cls, landscape):
        return

    def load(self, landscapefile):
        return

class SonosLandscape(Landscape):
    """
    """

    landscape_description = SonosLandscapeDescription

    def __init__(self):
        """
            This is a Singleton initializer.  It should only initialize variables the first time through.
        """
        this_cls = type(self)
        if not this_cls._initialized:
            self._expected_device_table = None
            super(SonosLandscape, self).__init__()
        return

    def initialize(self):
        """
            Called by '__init__' once at the beginning of the lifetime of a Landscape derived
            type.  This allows the derived types to participate in a customized intialization
            process.
        """
        super(SonosLandscape, self).initialize()
        return
    
    def diagnostic(self, diaglabel, diags):
        """
            Can be called in order to perform a diagnostic capture across the test landscape.

            :param diaglabel: The label to use for the diagnostic.
            :type diaglabel: str
            :param diags: A dictionary of diagnostics to run.
            :type diags: dict
        """
        super(SonosLandscape, self).diagnostic(diaglabel, diags)
        return
    
    def first_contact(self):
        """
            This method should be called as early as possible in order to ensure the entities in the
            automation landscape exist and the authentication credentials provided for these entities
            are valid and usable to interact with these entities.

            :returns list: list of failing entities
        """
        super(SonosLandscape, self).first_contact()

        self._validate_landscape()

        return

    def _validate_landscape(self):
        """
            This method is overriden in order to validate the info found
            in the landscape file.

            :param linfo: A python dictionary with the information contained in
                          the landscape.json file.
            :type linfo:  dict
        """
        if "pod" not in self.landscape_info:
            raise AKitConfigurationError("The 'testlandscape.py' file requires an 'pod' member.")

        pod_info = self.landscape_info["pod"]

        if "reference" not in pod_info:
            raise AKitConfigurationError("The 'testlandscape.py' file 'pod' data requires an 'reference' member.")

        ref_info = pod_info["reference"]

        if "ip" not in ref_info:
            raise AKitConfigurationError("The 'testlandscape.py' file 'pod->reference' data requires an 'ip' member.")
        if "port" not in ref_info:
            raise AKitConfigurationError("The 'testlandscape.py' file 'pod->reference' data requires an 'port' member.")

        return