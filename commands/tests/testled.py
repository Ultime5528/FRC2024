from utils.testcommand import TestCommand


class TestLED(TestCommand):
    def __init__(self, led):
        super().__init__()
        self.addRequirements(led)
        self.led = led

    def isFinished(self) -> bool:
        return True