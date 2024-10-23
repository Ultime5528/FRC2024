from utils.fault import ErrorType
from utils.property import autoproperty
from utils.testcommand import TestCommand


class TestDrivetrain(TestCommand):
    max_swerve_temperature = autoproperty(45.0)

    def __init__(self, drivetrain):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain

    def initialize(self):
        swervemotors = {
            "FL": self.drivetrain.swerve_module_fl,
            "FR": self.drivetrain.swerve_module_fr,
            "BL": self.drivetrain.swerve_module_bl,
            "BR": self.drivetrain.swerve_module_br,
        }
        for motorlocation, motor in swervemotors.items():
            if (
                motor._drive_motor.getMotorTemperature() > self.max_swerve_temperature
                or motor._turning_motor.getMotorTemperature()
                > self.max_swerve_temperature
            ):
                self.drivetrain.registerFault(
                    motorlocation
                    + " Swerve temperature is high. Let swerves cool down. ("
                    + str(motor._drive_motor.getMotorTemperature())
                    + "°C, "
                    + str(motor._turning_motor.getMotorTemperature())
                    + "°C)",
                    ErrorType.WARNING,
                )

            if not motor._drive_motor.isAlive() or not motor._turning_motor.isAlive():
                self.drivetrain.registerFault(
                    motorlocation
                    + " motor connection timed out. Check motor connection.",
                    ErrorType.ERROR,
                )

    def isFinished(self):
        return True
