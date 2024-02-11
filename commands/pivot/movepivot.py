from subsystems.pivot import Pivot
from utils.property import autoproperty, FloatProperty, asCallable
from utils.safecommand import SafeCommand
from utils.trapezoidalmotion import TrapezoidalMotion


class MovePivot(SafeCommand):
    @classmethod
    def toAmp(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: properties.position_amp)
        cmd.setName(cmd.getName() + ".toAmp")
        return cmd

    @classmethod
    def toSpeakerClose(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: properties.position_speaker_close)
        cmd.setName(cmd.getName() + ".toSpeakerClose")
        return cmd

    @classmethod
    def toSpeakerFar(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: properties.position_speaker_far)
        cmd.setName(cmd.getName() + ".toSpeakerFar")
        return cmd

    @classmethod
    def toLoading(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: properties.position_loading)
        cmd.setName(cmd.getName() + ".toLoading")
        return cmd

    def __init__(self, pivot: Pivot, end_position: FloatProperty):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.pivot = pivot
        self.addRequirements(pivot)

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.pivot.getHeight(),
            end_position=self.end_position_getter(),
            start_speed=max(properties.min_speed, abs(self.pivot.getMotorInput())),
            end_speed=properties.min_speed,
            max_speed=properties.max_speed,
            accel=properties.acceleration
        )

    def execute(self):
        height = self.pivot.getHeight()
        self.motion.setPosition(height)
        self.pivot.setSpeed(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished()

    def end(self, interrupted: bool) -> None:
        self.pivot.stop()


class _ClassProperties:
    # Pivot Properties #
    position_amp = autoproperty(70.0, subtable=MovePivot.__name__)
    position_speaker_far = autoproperty(155.0, subtable=MovePivot.__name__)
    position_speaker_close = autoproperty(232.0, subtable=MovePivot.__name__)
    position_loading = autoproperty(100, subtable=MovePivot.__name__)

    min_speed = autoproperty(0.1, subtable=MovePivot.__name__)
    max_speed = autoproperty(0.95, subtable=MovePivot.__name__)
    acceleration = autoproperty(0.035, subtable=MovePivot.__name__)


properties = _ClassProperties()
