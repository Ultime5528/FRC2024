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
    speed_far = autoproperty(0.40)
    speed_close = autoproperty(0.10)

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

        self.timer = wpilib.Timer()

        self.is_note_close = False

    def initialize(self):
        self.timer.reset()

    def execute(self):
        target = self.vision.getBestNote()

        if target is not None:
            self.timer.stop()
            self.timer.reset()

            # si le target est sous la croix rouge
            if target.getPitch() < 0:
                self.is_note_close = True

            self.vel_rot = self.p * (self.horizontal_offset - target.getYaw())
            self.drivetrain.drive(
                self.speed_far, 0, self.vel_rot, is_field_relative=False
            )
        elif self.is_note_close:
            self.timer.start()
            self.drivetrain.drive(self.speed_close, 0, 0, is_field_relative=False)
        else:
            self.is_note_close = False
            self.timer.start()

            print("target is none")

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay

    def end(self, interrupted: bool):
        self.drivetrain.stop()
        self.timer.stop()
