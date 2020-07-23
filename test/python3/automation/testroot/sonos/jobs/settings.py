
from akit.testing.testjob import TestJob

class SettingsJob(TestJob):

    # Friendly name for the test job
    name = "Settings Job"

    # Description of the job
    description = "This job runs the settings tests"

    # The test packs or tests that are included in this TestJob
    includes = [
        "sonos.testpacks.settings"
    ]

    # The tests that are to be excluded from this TestJob
    excludes = None
