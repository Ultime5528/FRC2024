from subsystems.pivot import Pivot
from utils.property import FloatProperty, asCallable
from utils.safecommand import SafeCommand


class ForceResetPivot(SafeCommand):
    @classmethod
    def toMax(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: pivot.height_max)
        cmd.setName(cmd.getName() + ".toMax")
        return cmd

    @classmethod
    def toMin(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: pivot.height_min)
        cmd.setName(cmd.getName() + ".toMin")
        return cmd

    def __init__(self, pivot: Pivot, reset_value: FloatProperty):
        super().__init__()
        self.pivot = pivot
        self.addRequirements(pivot)
        self._get_reset_value = asCallable(reset_value)

    def initialize(self):
        self.pivot.setHeight(self._get_reset_value())

    def isFinished(self) -> bool:
        return True
