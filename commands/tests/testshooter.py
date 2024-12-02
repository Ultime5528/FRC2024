from wpilib import PowerDistribution

import ports
from utils.fault import Severity
from utils.property import autoproperty
from utils.testcommand import TestCommand
import wpilib


class TestShooter(TestCommand):
    time_window = autoproperty(0.25)

    def __init__(self, shooter, pdp: PowerDistribution):
        super().__init__()
        self.addRequirements(shooter)
        self.shooter = shooter
        self.pdp = pdp
        self.left_shooter_current = ports.current_shooter_motor_gauche
        self.right_shooter_current = ports.current_shooter_motor_droite
        self.timer = wpilib.Timer

    def initialize(self):
        self.timer.restart()

        self.first_current_left = self.pdp.getCurrent(self.left_shooter_current)
        self.first_current_right = self.pdp.getCurrent(self.right_shooter_current)

        self.first_velocity_left = self.shooter._encoder_left.getVelocity()
        self.first_velocity_right = self.shooter._encoder_right.getVelocity()

    def execute(self):
        self.shooter.shoot()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.time_window

    def end(self, interrupted: bool):
        if self.pdp.getCurrent(self.left_shooter_current) <= self.first_current_left:
            self.shooter.registerFault(
                "Left shooter motor timed out. Check for connections", Severity.ERROR
            )
        if self.pdp.getCurrent(self.right_shooter_current) <= self.first_current_right:
            self.shooter.registerFault(
                "Right shooter motor timed out. Check for connections", Severity.ERROR
            )
        if self.shooter._encoder_left.getVelocity() <= self.first_velocity_left:
            self.shooter.registerFault(
                "Left shooter encoder timed out. Check for connections", Severity.ERROR
            )
        if self.shooter._encoder_right.getVelocity() <= self.first_velocity_right:
            self.shooter.registerFault(
                "Right shooter encoder timed out. Check for connections", Severity.ERROR
            )

        self.shooter.stop()
