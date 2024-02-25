from subsystems.shooter import Shooter
from utils.property import autoproperty
from utils.safecommand import SafeCommand


class ManualShoot(SafeCommand):
    rpm = autoproperty(5000.0)

    def __init__(self, shooter: Shooter):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(shooter)

    def execute(self):
        self.shooter.shoot(rpm=self.rpm)

    def end(self, interrupted: bool):
        self.shooter.stop()
