import rev
from wpilib import RobotBase
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureFollower, configureLeader


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

        self._ref_rpm = 0.0
        self._reached_speed = False

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self._left_motor)
            self.right_motor_sim = SparkMaxSim(self._right_motor)

    def shoot(self, rpm: float):
        self._pid.setReference(rpm, rev.CANSparkMax.ControlType.kVelocity)
        self._ref_rpm = rpm

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

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addBooleanProperty("reached_speed", lambda: self._reached_speed, noop)
        builder.addFloatProperty("velocity", self._encoder.getVelocity, noop)
        builder.addFloatProperty("ref_rpm", lambda: self._ref_rpm, noop)
