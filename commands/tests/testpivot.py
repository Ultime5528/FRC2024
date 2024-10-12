from utils.testcommand import TestCommand


class TestPivot(TestCommand):
    def __init__(self, pivot):
        super().__init__()
        self.addRequirements(pivot)
        self.pivot = pivot

    def isFinished(self) -> bool:
        return True