import rev
import wpilib

from wpilib import RobotBase
import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim


class Climber(SafeSubsystem):
    climber_speed_up = autoproperty(0.25)
    climber_speed_down = autoproperty(-0.25)

    def __init__(self):
        super().__init__()
        self.motor_left = rev.CANSparkMax(ports.climber_motor_left,
                                    rev.CANSparkMax.MotorType.kBrushless)
        self.motor_right = rev.CANSparkMax(ports.climber_motor_right,
                                    rev.CANSparkMax.MotorType.kBrushless)

        if RobotBase.isSimulation():
            self.motor_right_sim = SparkMaxSim(self.motor_right)
            self.motor_left_sim = SparkMaxSim(self.motor_left)

    def extendLeft(self):
        self.motor_left.set(self.climber_speed_up)

    def retractLeft(self):
        self.motor_left.set(self.climber_speed_down)

    def stopLeft(self):
        self.motor_left.set(0)

    def extendRight(self):
        self.motor_right.set(self.climber_speed_up)

    def retractRight(self):
        self.motor_right.set(self.climber_speed_down)

    def stopRight(self):
        self.motor_right.set(0)

