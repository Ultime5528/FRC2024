import rev
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

    def __init__(self):
        super().__init__()

        self.left_motor = rev.CANSparkMax(ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(self.left_motor, "brake")

        self.right_motor = rev.CANSparkMax(ports.shooter_motor_right, rev.CANSparkMax.MotorType.kBrushless)
        configureFollower(self.right_motor, self.left_motor, "brake", inverted=True)

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self.left_motor)
            self.right_motor_sim = SparkMaxSim(self.right_motor)

    def simulationPeriodic(self) -> None:
        self.left_motor_sim.setVelocity(self.left_motor.get())
        self.right_motor_sim.setVelocity(-self.left_motor.get())

    def shootHigh(self):
        self.left_motor.set(self.shooter_high_speed)

    def shootLow(self):
        self.left_motor.set(self.shooter_low_speed)
