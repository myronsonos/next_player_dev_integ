
from akit.testing.testcontainer import BrickTestContainer

from sonos.testpacks.settings.settingstestpack import SettingsTestPack


class SystemSettingsTests(BrickTestContainer, SettingsTestPack):
    """
        This test container groups the system settings tests
    """

    def test_firstsettings(self):
        print("test_firstsettings ran...")
        return