from typing import Union, Callable, Optional

from commands2.button import CommandXboxController
from wpilib import DriverStation
from wpilib.interfaces import GenericHID
from wpimath.filter import SlewRateLimiter

from commands.drivetrain.drive import apply_center_distance_deadzone, properties
from subsystems.drivetrain import Drivetrain
from subsystems.vision2 import Vision2
from utils.property import autoproperty
from utils.safecommand import SafeCommand

class GoToNote(SafeCommand):
    p = autoproperty(0.025)
    horizontal_offset = autoproperty(5.0)

    def __init__(
        self,
        drivetrain: Drivetrain,
        vision: Vision2,
    ):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.vision = vision
        self.vel_rot = 0

        self.m_xspeedLimiter = SlewRateLimiter(3)
        self.m_yspeedLimiter = SlewRateLimiter(3)

    def execute(self):
        target = self.vision.getBestNote()
        y_speed = -0.5

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            y_speed *= -0.5

        y_speed = self.m_yspeedLimiter.calculate(y_speed)
        # TODO: quand le robot voit plus de note, le il arrete de boujer. Il devrait continuer le bouger vers l'avant
        if target is not None:
            print('la target est traquée')
            self.vel_rot = self.p * (self.horizontal_offset - target.getYaw())
            self.drivetrain.drive(
                        0.15, 0, self.vel_rot, is_field_relative=False
            )
        else:
            self.drivetrain.drive(
                0, 0, 0, is_field_relative=True
            )
            print("target is none")

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool):
        self.drivetrain.stop()