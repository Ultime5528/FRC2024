
import rev

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem


class Intake(SafeSubsystem):
    speed_in = autoproperty(0.3)
    speed_out = autoproperty(-0.17)

    def __init__(self):
        super().__init__()
        self.motor = rev.CANSparkMax(ports.intake_motor, rev.CANSparkMax.MotorType.kBrushless)

    def takeIn(self):
        self.motor.set(self.speed_in)

    def stop(self):
        self.motor.stopMotor()

    def takeOut(self):
        self.motor.set(self.speed_out)
