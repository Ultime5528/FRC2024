from subsystems.intake import Intake
from utils.safecommand import SafeCommand


class Load(SafeCommand):
    def __init__(self, intake: Intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake

    def execute(self) -> None:
        self.intake.load()

    def isFinished(self) -> bool:
        return False

    def end(self, interrupted: bool) -> None:
        self.intake.stop()
