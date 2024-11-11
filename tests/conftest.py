import pytest

from utils.safesubsystem import SafeSubsystem


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    for subsystem in SafeSubsystem.subsystems:
        subsystem._test_command = None
        subsystem._subsystem_status_prop = None
        subsystem._faults_prop = None
    SafeSubsystem.subsystems = []
    SafeSubsystem.subsystems_tests = []
