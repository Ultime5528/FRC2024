import rev
import wpilib
from wpilib import RobotBase
import commands2
import ports
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxutils import configureFollower, configureLeader
from utils.sparkmaxsim import SparkMaxSim


class Shooter(SafeSubsystem):

    def __init__(self):
        super().__init__()

        self._left_motor = rev.CANSparkMax(
            ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless
        )
        configureLeader(self._left_motor, "coast")

        self._right_motor = rev.CANSparkMax(
            ports.shooter_motor_right, rev.CANSparkMax.MotorType.kBrushless
        )
        configureFollower(self._right_motor, self._left_motor, "coast", inverted=True)

        self._encoder = self._left_motor.getEncoder()

        self._reached_speed = False

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self._left_motor)
            self.right_motor_sim = SparkMaxSim(self._right_motor)

    def shoot(self, rpm: float):
        self._left_motor.set(rpm)

        if self._encoder.getVelocity() >= rpm:
            self._reached_speed = True
        else:
            self._reached_speed = False

    def reachedSpeed(self):
        return self._reached_speed

    def stop(self):
        self._left_motor.stopMotor()
        self._reached_speed = False

    def simulationPeriodic(self):
        self.left_motor_sim.setVelocity(self._left_motor.get())
        self.right_motor_sim.setVelocity(-self._left_motor.get())
