import wpilib
from utils.safecommand import SafeCommand
from subsystems.intake import Intake
from utils.property import autoproperty


class Load(SafeCommand):
    intake_time = autoproperty(1)

    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(Intake)
        self.intake = intake
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.intake.takeOut()

    def isFinished(self) -> bool:
        return self.timer.get() >= self.open_time

    def end(self, interrupted: bool) -> None:
        self.timer.stop()
        self.intake.stop()
