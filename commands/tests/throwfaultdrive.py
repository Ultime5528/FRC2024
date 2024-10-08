from subsystems.drivetrain import Drivetrain
from utils.fault import Fault, ErrorType
from utils.safecommand import SafeCommand


class ThrowFaultDrive(SafeCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        self.drivetrain.registerFault(Fault("FL Swerve should not be over 35 degrees celsius", False, ErrorType.WARNING))

    def isFinished(self) -> bool:
        return True