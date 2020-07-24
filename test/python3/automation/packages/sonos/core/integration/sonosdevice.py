


class SonosDevice(IntegrationMixIn):

    def __init__(self, upnp_device, *args, role=None, **kwargs):
        self._upnp_device = upnp_device
        super(SonosDeviceMixIn)
        return