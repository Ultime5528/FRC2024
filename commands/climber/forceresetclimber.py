from subsystems.climber import Climber
from utils.property import FloatProperty, asCallable
from utils.safecommand import SafeCommand


class ForceResetClimber(SafeCommand):
    @classmethod
    def toMax(cls, climber: Climber):
        cmd = cls(climber, lambda: climber.properties.height_max)
        cmd.setName(cmd.getName() + ".toMax")
        return cmd

    @classmethod
    def toMin(cls, climber: Climber):
        cmd = cls(climber, lambda: climber.properties.height_min)
        cmd.setName(cmd.getName() + ".toMin")
        return cmd

    def __init__(self, climber: Climber, reset_value: FloatProperty):
        super().__init__()
        self.climber = climber
        self.addRequirements(climber)
        self._get_reset_value = asCallable(reset_value)

    def initialize(self):
        self.climber.setHeight(self._get_reset_value())

    def isFinished(self) -> bool:
        return True
