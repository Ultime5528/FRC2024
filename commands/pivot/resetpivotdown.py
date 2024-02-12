from subsystems import pivot
from subsystems.pivot import Pivot
from utils.safecommand import SafeCommand


class ResetPivotDown(SafeCommand):
    def __init__(self, pivot: Pivot):
        super().__init__()
        self.pivot = pivot
        self.addRequirements(pivot)
        self.switch_down_was_pressed = False

    def initialize(self):
        self.switch_down_was_pressed = False

    def execute(self):
        if self.pivot.isDown():  # If the down switch is pressed move up.
            self.pivot.moveUp()
            self.switch_down_was_pressed = True
        else:
            self.pivot.moveDown()  # if switch is not pressed move down until pressed.

    def isFinished(self) -> bool:
        return not self.pivot.isDown() and self.switch_down_was_pressed

    def end(self, interrupted: bool):
        pivot.has_reset = True
        self.pivot.stop()
