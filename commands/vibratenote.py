from typing import NewType

from wpilib import Timer

from subsystems.controller import Controller
from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand


NoReqIntake = NewType("NoReqIntake", Intake)


class VibrateNote(SafeCommand):
    delay_vibrate = autoproperty(0.1)
    delay_wait = autoproperty(0.6)
    rumble_force = autoproperty(0.5)

    def __init__(self, controller: Controller, intake: NoReqIntake):
        super().__init__()
        self.controller = controller
        self.intake = intake
        self.addRequirements(controller)
        self.timer = Timer()

    def initialize(self):
        self.timer.restart()

    def execute(self):
        if self.intake.hasNote():
            if self.timer.get() < self.delay_vibrate:
                self.controller.vibrate(self.rumble_force)
            elif self.timer.get() > self.delay_vibrate+self.delay_wait:
                self.timer.restart()
            else:
                self.controller.vibrate(0)

    def end(self, interrupted: bool):
        self.controller.vibrate(0)
