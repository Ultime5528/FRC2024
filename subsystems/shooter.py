import rev
import wpilib
from wpilib import RobotBase
import commands2
import ports
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxutils import configureFollower, configureLeader
from utils.sparkmaxsim import SparkMaxSim
from utils.property import autoproperty


class Shooter(SafeSubsystem):
    shooter_high_speed = autoproperty(0.5)
    shooter_low_speed = autoproperty(0.25)
    shooter_angle_up_speed = autoproperty(0.2)
    shooter_angle_down_speed = autoproperty(-0.2)

    def __init__(self):
        super().__init__()

        self.left_motor = rev.CANSparkMax(ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(self.left_motor, "brake")

        self.right_motor = rev.CANSparkMax(ports.shooter_motor_right, rev.CANSparkMax.MotorType.kBrushless)
        configureFollower(self.right_motor, self.left_motor, "brake", inverted=True)

        self.pivot_motor = wpilib.VictorSP(ports.shooter_pivot_motor)
        self.pivot_encoder = self.pivot_motor.getEncoder()

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self.left_motor)
            self.right_motor_sim = SparkMaxSim(self.right_motor)
            self.pivot_motor_sim = SparkMaxSim(self.pivot_motor)

    def angleUp(self):
        self.pivot_motor.set(autoproperty(self.shooter_angle_up_speed))

    def angleDown(self):
        self.pivot_motor.set(autoproperty(self.shooter_angle_down_speed))

    def shootHigh(self):
        self.left_motor.set(self.shooter_high_speed)

    def shootLow(self):
        self.left_motor.set(self.shooter_low_speed)
