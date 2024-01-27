import wpilib
import phoenix5
import ports
from utils.safesubsystem import SafeSubsystem
from utils.property import autoproperty


class Pivot(SafeSubsystem):
    up_speed = autoproperty(0.5)
    down_speed = autoproperty(-0.5)

    def __init__(self):
        super().__init__()

        self.high_limitswitch = wpilib.DigitalInput(ports.pivot_limitswitch_high)
        self.low_limitswitch = wpilib.DigitalInput(ports.pivot_limitswitch_low)

        self.motor = phoenix5.WPI_VictorSPX(ports.pivot_motor)
        self.encoder = wpilib.Encoder(ports.pivot_encoder_a, ports.pivot_encoder_b)

    def moveUp(self):
        self.motor.set(self.up_speed)

    def moveDown(self):
        self.motor.set(self.down_speed)
