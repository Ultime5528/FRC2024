from utils.testcommand import TestCommand


class TestController(TestCommand):
    def __init__(self, controller):
        super().__init__()
        self.addRequirements(controller)
        self.controller = controller

    def isFinished(self) -> bool:
        return True