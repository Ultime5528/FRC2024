from typing import Union, Callable, Optional

import wpilib
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
    p = autoproperty(0.015)
    horizontal_offset = autoproperty(2.0)
    delay = autoproperty(1.0)

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
        self.timer = wpilib.Timer()

        self.noteisclose = False

    def initialize(self):
        self.timer.reset()

    def execute(self):
        target = self.vision.getBestNote()
        y_speed = -0.5

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            y_speed *= -0.5

        y_speed = self.m_yspeedLimiter.calculate(y_speed)
        # TODO: quand le robot voit plus de note, le il arrete de boujer. Il devrait continuer le bouger vers l'avant
        if target is not None:
            self.timer.stop()
            self.timer.reset()

            # si le target est sous la croix rouge
            if target.getPitch() < 0:
                self.noteisclose = True

            self.vel_rot = self.p * (self.horizontal_offset - target.getYaw())
            self.drivetrain.drive(
                        0.40, 0, self.vel_rot, is_field_relative=False
            )
        elif self.noteisclose == True:
            self.timer.start()
            self.drivetrain.drive(
                0.10, 0, 0, is_field_relative=False
            )
        else:
            self.noteisclose = False
            self.timer.start()

            print("target is none")

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        self.timer.stop()