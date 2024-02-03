from subsystems.pivot import Pivot
from utils.safecommand import SafeCommand


class ResetPivot(SafeCommand):
    def __init__(self, pivot: Pivot,):
        super().__init__()
        self.addRequirements(pivot)
        self.pivot = pivot
        self.switch_up_was_pressed = False

    def initialize(self):
        self.switch_up_was_pressed = False

    def execute(self):
        if not self.pivot.isUp():
            self.pivot.moveUp()
        elif self.pivot.isUp():
            self.pivot.moveDown()
            self.switch_up_was_pressed = True
        else:
            assert False, "Should not go in the else clause"

    def isFinished(self) -> bool:
        return not self.pivot.isUp() and self.switch_up_was_pressed

    def end(self, interrupted: bool):
        self.pivot.stop()
        self.pivot.resetEncoder()
