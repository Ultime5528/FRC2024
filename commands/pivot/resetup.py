from subsystems.pivot import Pivot
from utils.safecommand import SafeCommand


class ResetPivot(SafeCommand):
    def __init__(self, pivot: Pivot):
        super().__init__()
        self.pivot = pivot
        self.addRequirements(pivot)
        self.switch_up_was_pressed = False

    def initialize(self):
        self.switch_up_was_pressed = False

    def execute(self):
        if self.pivot.isUp():  # If the up switch is pressed move down.
            self.pivot.moveDown()
            self.switch_up_was_pressed = True
        else:
            self.pivot.moveUp()  # if switch is not pressed move up until pressed.

    def isFinished(self) -> bool:
        return not self.pivot.isUp() and self.switch_up_was_pressed

    def end(self, interrupted: bool):
        self.pivot.stop()
