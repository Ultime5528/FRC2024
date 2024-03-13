from typing import NewType

import wpilib

from subsystems.controller import Controller
from subsystems.intake import Intake
from utils.coroutinecommand import CoroutineCommand
from utils.property import autoproperty

NoReqIntake = NewType("NoReqIntake", Intake)


class VibrateNote(CoroutineCommand):
    first_rumble_delay = autoproperty(1.0)
    first_rumble_force = autoproperty(0.8)
    rumble_wait = autoproperty(0.7)
    next_rumble_delay = autoproperty(0.15)
    next_rumble_force = autoproperty(0.3)

    def __init__(self, controller: Controller, intake: NoReqIntake):
        super().__init__()
        self.controller = controller
        self.intake = intake
        self.addRequirements(controller)
        self.timer = wpilib.Timer()

    def coroutine(self):
        while not self.intake.hasNote():
            yield

        self.timer.restart()
        while not self.timer.hasElapsed(self.first_rumble_delay):
            self.controller.vibrate(self.first_rumble_force)
            yield

        while True:
            self.timer.restart()
            while not self.timer.hasElapsed(self.rumble_wait):
                self.controller.vibrate(0)
                yield

            self.timer.restart()
            while not self.timer.hasElapsed(self.next_rumble_delay):
                self.controller.vibrate(self.next_rumble_force)
                yield

    def isFinished(self) -> bool:
        return not self.intake.hasNote()

    def end(self, interrupted: bool):
        self.controller.vibrate(0)
