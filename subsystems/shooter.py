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
    high_speed = autoproperty(0.5)
    low_speed = autoproperty(0.25)

    def __init__(self):
        super().__init__()

        self.left_motor = rev.CANSparkMax(ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(self.left_motor, "coast")

        self.right_motor = rev.CANSparkMax(ports.shooter_motor_right, rev.CANSparkMax.MotorType.kBrushless)
        configureFollower(self.right_motor, self.left_motor, "coast", inverted=True)

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self.left_motor)
            self.right_motor_sim = SparkMaxSim(self.right_motor)

    def shootHigh(self):
        self.left_motor.set(self.high_speed)

    def shootLow(self):
        self.left_motor.set(self.low_speed)

    def simulationPeriodic(self):
        self.left_motor_sim.setVelocity(self.left_motor.get())
        self.right_motor_sim.setVelocity(-self.left_motor.get())
