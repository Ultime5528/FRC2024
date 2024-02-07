from subsystems.climber import Climber
from utils.safecommand import SafeCommand
from utils.property import autoproperty, FloatProperty, asCallable
from utils.trapezoidalmotion import TrapezoidalMotion


class ForceResetClimber(SafeCommand):
    @classmethod
    def toMax(cls, climber: Climber):
        cmd = cls(climber, lambda: properties.position_max)
        cmd.setName(cmd.getName() + ".toMax")
        return cmd

    @classmethod
    def toZero(cls, climber: Climber):
        cmd = cls(climber, lambda: properties.position_zero)
        cmd.setName(cmd.getName() + ".toZero")
        return cmd

    def __init__(self, climber: Climber, end_position: FloatProperty):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.climber = climber
        self.addRequirements(climber)

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.climber.getHeight(),
            end_position=self.end_position_getter(),
            start_speed=max(properties.min_speed, abs(self.climber.getMotorSpeed())),
            end_speed=properties.min_speed,
            max_speed=properties.max_speed,
            accel=properties.acceleration
        )
        self.finished = False

    def execute(self):
        if self.motion.isFinished():
            self.climber.stop()
        else:
            current_elevation = self.climber.getHeight()
            self.motion.setPosition(current_elevation)
            self.climber._motor.set(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished()

    def end(self, interrupted: bool) -> None:
        self.climber.stop()


class _ClassProperties:
    # climber properties #
    position_max = autoproperty(100, subtable=ForceResetClimber.__name__)
    position_zero = autoproperty(0, subtable=ForceResetClimber.__name__)
    min_speed = autoproperty(0.1, subtable=ForceResetClimber.__name__)
    max_speed = autoproperty(0.95, subtable=ForceResetClimber.__name__)
    acceleration = autoproperty(0.035, subtable=ForceResetClimber.__name__)


properties = _ClassProperties
