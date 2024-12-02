import wpilib
from wpilib import PowerDistribution

import ports
import subsystems.drivetrain
from utils.swerve import SwerveModule
from subsystems.drivetrain import Drivetrain
from utils.fault import Severity
from utils.property import autoproperty
from utils.testcommand import TestCommand


class TestDrivetrain(TestCommand):
    max_swerve_temperature = autoproperty(45.0)
    time_window = autoproperty(0.25)

    def __init__(self, drivetrain: Drivetrain, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.pdp = pdp
        self.timer = wpilib.Timer()

        self.current_swerve_turn = [
            ports.current_swerve_turning_fr,
            ports.current_swerve_turning_fl,
            ports.current_swerve_turning_br,
            ports.current_swerve_turning_bl,
        ]

        self.current_swerve_motor = [
            ports.current_swerve_motor_fr,
            ports.current_swerve_motor_fl,
            ports.current_swerve_motor_br,
            ports.current_swerve_motor_bl,
        ]

        self.swervemotors = {
            "FL": self.drivetrain.swerve_module_fl,
            "FR": self.drivetrain.swerve_module_fr,
            "BL": self.drivetrain.swerve_module_bl,
            "BR": self.drivetrain.swerve_module_br,
        }

    def initialize(self):
        self.timer.start()

        self.first_turn_current = [
            self.pdp.getCurrent(ports.current_swerve_turning_fl),
            self.pdp.getCurrent(ports.current_swerve_turning_fr),
            self.pdp.getCurrent(ports.current_swerve_turning_bl),
            self.pdp.getCurrent(ports.current_swerve_turning_br),
        ]

        self.first_motor_current = [
            self.pdp.getCurrent(ports.current_swerve_motor_fl),
            self.pdp.getCurrent(ports.current_swerve_motor_fr),
            self.pdp.getCurrent(ports.current_swerve_motor_bl),
            self.pdp.getCurrent(ports.current_swerve_motor_br),
        ]

        for motorlocation, motor in self.swervemotors.items():
            if motor._turning_motor.getMotorTemperature() > self.max_swerve_temperature:
                self.drivetrain.registerFault(
                    "High swerve temperature on "
                    + motorlocation
                    + " Turning motor. Let swerves cool down. ("
                    + str(motor._turning_motor.getMotorTemperature())
                    + "°C)",
                    Severity.WARNING,
                )
            elif motor._drive_motor.getMotorTemperature() > self.max_swerve_temperature:
                self.drivetrain.registerFault(
                    "High swerve temperature on "
                    + motorlocation
                    + " Driving motor. Let swerves cool down. ("
                    + str(motor._drive_motor.getMotorTemperature())
                    + "°C)",
                    Severity.WARNING,
                )

    def execute(self):
        for motorlocation, motor in self.swervemotors.items():
            motor._turning_motor.set(self.drivetrain.max_angular_speed)
            motor._drive_motor.set(self.drivetrain.swerve_module_fl.max_speed)

    def isFinished(self) -> bool:
        return self.timer.get() >= self.time_window

    def end(self, interrupted: bool):
        self.swerve_property = zip(
            self.current_swerve_turn,
            self.current_swerve_motor,
            self.first_turn_current,
            self.first_motor_current,
            self.swervemotors,
        )
        for swerves in self.swerve_property:
            if self.pdp.getCurrent(swerves[0]) <= swerves[2]:
                self.drivetrain.registerFault(
                    "Swerve"
                    + swerves[4][0]
                    + "turning motor timed out. Check connections",
                    Severity.ERROR,
                )
            if self.pdp.getCurrent(swerves[1]) <= swerves[3]:
                self.drivetrain.registerFault(
                    "Swerve"
                    + swerves[4][0]
                    + "driving motor timed out. Check connections",
                    Severity.ERROR,
                )

        for motorlocation, motor in self.swervemotors.items():
            motor._turning_motor.stopMotor()
            motor._drive_motor.stopMotor()
