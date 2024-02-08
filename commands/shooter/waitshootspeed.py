from utils.safecommand import SafeCommand
from subsystems.shooter import Shooter


type NoReqShooter = Shooter

class WaitShootSpeed(SafeCommand):
    def __init__(self, shooter: NoReqShooter):
        super().__init__()
        self._shooter = shooter

    def isFinished(self) -> bool:
        return self._shooter.reachedSpeed()
