from commands2 import ProxyCommand

from subsystems.pivot import Pivot
from utils.safecommand import SafeCommand


class MaintainPivot(SafeCommand):
    def __init__(self, pivot: Pivot):
        super().__init__()
        self.pivot = pivot

    def execute(self):
        if (
            self.pivot.state == Pivot.State.SpeakerClose
            or self.pivot.State == Pivot.State.SpeakerFar
            or self.pivot.State == Pivot.State.Amp
        ):
            self.pivot.maintain()
