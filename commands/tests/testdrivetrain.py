from utils.fault import Fault, ErrorType
from utils.safecommand import SafeCommand


class TestDrivetrain(SafeCommand):
    def __init__(self, drivetrain):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain

    def initialize(self):
        self.drivetrain.clearFaults()
        self.drivetrain.registerFault(Fault("Test warning", False, ErrorType.WARNING))
        self.drivetrain.registerFault(Fault("Test error", False, ErrorType.ERROR))

    def isFinished(self):
        return True