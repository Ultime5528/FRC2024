from utils.testcommand import TestCommand


class TestIntake(TestCommand):
    def __init__(self, intake):
        super().__init__()
        self.addRequirements(intake)
        self.intake = intake

    def isFinished(self) -> bool:
        return True