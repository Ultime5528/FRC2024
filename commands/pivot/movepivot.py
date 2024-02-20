import wpilib

from subsystems.pivot import Pivot
from utils.property import autoproperty, FloatProperty, asCallable
from utils.safecommand import SafeCommand
from utils.trapezoidalmotion import TrapezoidalMotion


class MovePivot(SafeCommand):
    @classmethod
    def toAmp(cls, pivot: Pivot):
        cmd = cls(pivot, lambda: move_pivot_properties.position_amp, Pivot.State.Amp)
        cmd.setName(cmd.getName() + ".toAmp")
        return cmd

    @classmethod
    def toSpeakerClose(cls, pivot: Pivot):
        cmd = cls(
            pivot,
            lambda: move_pivot_properties.position_speaker_close,
            Pivot.State.SpeakerClose,
        )
        cmd.setName(cmd.getName() + ".toSpeakerClose")
        return cmd

    @classmethod
    def toSpeakerFar(cls, pivot: Pivot):
        cmd = cls(
            pivot,
            lambda: move_pivot_properties.position_speaker_far,
            Pivot.State.SpeakerFar,
        )
        cmd.setName(cmd.getName() + ".toSpeakerFar")
        return cmd

    @classmethod
    def toLoading(cls, pivot: Pivot):
        cmd = cls(
            pivot, lambda: move_pivot_properties.position_loading, Pivot.State.Loading
        )
        cmd.setName(cmd.getName() + ".toLoading")
        return cmd

    def __init__(
        self, pivot: Pivot, end_position: FloatProperty, new_state: Pivot.State
    ):
        super().__init__()
        self.end_position_getter = asCallable(end_position)
        self.pivot = pivot
        self.addRequirements(pivot)
        self.new_state = new_state

    def initialize(self):
        self.motion = TrapezoidalMotion(
            start_position=self.pivot.getHeight(),
            end_position=self.end_position_getter(),
            start_speed=max(
                move_pivot_properties.speed_min, abs(self.pivot.getMotorInput())
            ),
            end_speed=move_pivot_properties.speed_min,
            max_speed=move_pivot_properties.speed_max,
            accel=move_pivot_properties.accel,
        )
        self.pivot.state = Pivot.State.Moving

    def execute(self):
        height = self.pivot.getHeight()
        self.motion.setPosition(height)
        self.pivot.setSpeed(self.motion.getSpeed())

    def isFinished(self) -> bool:
        return self.motion.isFinished() or not self.pivot.hasReset()

    def end(self, interrupted: bool) -> None:
        if not self.pivot.hasReset():
            wpilib.reportError("Pivot has not reset: cannot MovePivot")

        self.pivot.stop()

        if interrupted:
            self.pivot.state = Pivot.State.Invalid
        else:
            self.pivot.state = self.new_state


class _ClassProperties:
    # Pivot Properties #
    position_amp = autoproperty(48.0, subtable=MovePivot.__name__)
    position_speaker_far = autoproperty(20.0, subtable=MovePivot.__name__)
    position_speaker_close = autoproperty(30.0, subtable=MovePivot.__name__)
    position_loading = autoproperty(5.0, subtable=MovePivot.__name__)

    speed_min = autoproperty(0.1, subtable=MovePivot.__name__)
    speed_max = autoproperty(0.95, subtable=MovePivot.__name__)
    accel = autoproperty(0.035, subtable=MovePivot.__name__)


move_pivot_properties = _ClassProperties()
