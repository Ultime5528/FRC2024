import rev
import wpilib
from wpilib import RobotBase
import commands2
import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxutils import configureFollower, configureLeader
from utils.sparkmaxsim import SparkMaxSim


class Shooter(SafeSubsystem):
    p = autoproperty(0.001)
    i = autoproperty(0.0)
    d = autoproperty(0.0)
    ff = autoproperty(0.0)

    def __init__(self):
        super().__init__()

        self._left_motor = rev.CANSparkMax(
            ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless
        )
        configureLeader(self._left_motor, "coast")
        self._pid = self._left_motor.getPIDController()
        self._pid.setP(self.p)
        self._pid.setI(self.i)
        self._pid.setD(self.d)
        self._pid.setFF(self.ff)




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
        self._pid.setReference(rpm, rev.CANSparkMax.ControlType.kVelocity)

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
