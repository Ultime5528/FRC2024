import wpilib
from wpilib import PowerDistribution

import ports
import subsystems.drivetrain
from subsystems.drivetrain import Drivetrain
from utils.fault import ErrorType
from utils.property import autoproperty
from utils.testcommand import TestCommand


class TestDrivetrain(TestCommand):
    max_swerve_temperature = autoproperty(45.0)

    def __init__(self, drivetrain, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.pdp = pdp
        self.timer = wpilib.Timer

        self.current_swerve_turn = {
            ports.current_swerve_turning_fr,
            ports.current_swerve_turning_fl,
            ports.current_swerve_turning_br,
            ports.current_swerve_turning_bl,
        }

        self.current_swerve_motor = {
            ports.current_swerve_motor_fr,
            ports.current_swerve_motor_fl,
            ports.current_swerve_motor_br,
            ports.current_swerve_motor_bl,
        }

        self.swervemotors = {
            "FL": self.drivetrain.swerve_module_fl,
            "FR": self.drivetrain.swerve_module_fr,
            "BL": self.drivetrain.swerve_module_bl,
            "BR": self.drivetrain.swerve_module_br,
        }

    def initialize(self):
        self.timer.start()

        self.first_turn_current = self.pdp.getCurrent(self.current_swerve_turn)
        self.first_motor_current = self.pdp.getCurrent(self.current_swerve_motor)

        for motorlocation, motor in self.swervemotors.items():
            if (
                motor._drive_motor.getMotorTemperature() > self.max_swerve_temperature
                or motor._turning_motor.getMotorTemperature()
                > self.max_swerve_temperature
            ):
                self.drivetrain.registerFault(
                    "High swerve temperature on "
                    + motorlocation
                    + ". Let swerves cool down. ("
                    + str(motor._drive_motor.getMotorTemperature())
                    + "°C, "
                    + str(motor._turning_motor.getMotorTemperature())
                    + "°C)",
                    ErrorType.WARNING,
                )

    #    def execute(self):
    #        for motor_location, swerve in self.swervemotors.items():
    #            swerve

    def isFinished(self):
        return True
