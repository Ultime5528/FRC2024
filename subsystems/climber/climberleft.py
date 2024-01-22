import rev
import wpilib

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxutils import configureLeader


class ClimberLeft(SafeSubsystem):
    climber_speed_up = autoproperty(0.25)
    climber_speed_down = autoproperty(-0.25)

    def __init__(self):
        super().__init__()
        self.climb_motor_left = rev.CANSparkMax(ports.climber_motor_left,
                                                rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(self.climb_motor_left, "brake", False)

    def extend(self):
        self.climb_motor_left.set(self.climber_speed_up)

    def retract(self):
        self.climb_motor_left.set(self.climber_speed_down)

    def stop(self):
        self.climb_motor_left.set(0)
