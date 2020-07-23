
from akit.testing.testpack import TestPack

class SettingsTestPack(TestPack):

    name = "Settings TestPack"                        # TestPack Friendly Name
    description = "This is the settings test pack"    # TestPack Description

    def acclimate(self, testlandscape):
        """
            API called by the test framework in order to acclimate the :class:`TestPack` to the :class:`TestLandscape`.
            When this method is called on a :class:`TestPack` it can analyze the testlandscape and configure
            internal state that can be used to determine which tests are applicable to the given test
            landscape.
        """
        return 

    def expectations(self):
        """
            Method that can be implemented by derived classes or updated dynamically to reflect the
            expected torun and skipped test counts for a given testlandscape.  The test framework will call the 'acclimate'
            method prior to calling this method in order to let the 'TestPack' analyze the testlandscape
            and determine which tests are applicable to the test 

            (torun, skipped)
        """
        return

    def scopes_enter(self):
        """
        """
        super(SettingsTestPack).scope_enter()
        return
    
    def scopes_exit(self):
        """
        """
        super(SettingsTestPack).scope_exit()
        return