
import ports
from utils import safesubsystem
from utils.property import autoproperty
import rev


class Intake(safesubsystem):
    intake_speed = autoproperty(0.3)
    intake_reverse_speed = autoproperty((intake_speed/-1.3))
    def __init__(self):
        super().__init__()
        motor = rev.CANSparkMax(ports.intake_motor, rev.CANSparkMax.MotorType.kBrushless)

    def activate(self):
        self.motor.set(self.intake_speed)

    def stop(self):
        self.motor.stop()

    def reject(self):
        self.motor.set(self.intake_reverse_speed)
