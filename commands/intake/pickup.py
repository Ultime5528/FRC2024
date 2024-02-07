import wpilib

from subsystems.intake import Intake
from utils.property import autoproperty
from utils.safecommand import SafeCommand
import ports
from subsystems.led import LEDController, ModeLED


class PickUp(SafeCommand):
    delay_time = autoproperty(1.0)

    def __init__(self, intake: Intake, led_controller: LEDController):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake
        self.timer = wpilib.Timer()

        self.addRequirements(led_controller)
        self.led_controller = led_controller

    def initialize(self) -> None:
        self.timer.reset()

    def execute(self) -> None:
        self.intake.pickUp()
        self.led_controller.setMode(ModeLED.TAKING)
        if self.intake.hasNote():
            self.timer.start()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.delay_time

    def end(self, interrupted: bool) -> None:
        self.led_controller.setMode(ModeLED.NONE)
        self.timer.stop()
        self.intake.stop()
