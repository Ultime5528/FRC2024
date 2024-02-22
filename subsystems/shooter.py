import rev
from wpilib import RobotBase
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureLeader


def computeVoltage(rpm_goal, rpm_actual, p, ff) -> tuple[float, bool]:
    return p * (rpm_goal - rpm_actual) + ff * rpm_goal, rpm_actual >= rpm_goal


class Shooter(SafeSubsystem):
    p_left = autoproperty(0.002)
    ff_left = autoproperty(0.00218)

    p_right = autoproperty(0.002)
    ff_right = autoproperty(0.00198)

    def __init__(self):
        super().__init__()

        self._left_motor = rev.CANSparkMax(
            ports.shooter_motor_left, rev.CANSparkMax.MotorType.kBrushless
        )
        configureLeader(self._left_motor, "coast")
        self._left_motor.enableVoltageCompensation(12.0)
        self._encoder_left = self._left_motor.getEncoder()

        self._right_motor = rev.CANSparkMax(
            ports.shooter_motor_right, rev.CANSparkMax.MotorType.kBrushless
        )
        configureLeader(self._right_motor, "coast", inverted=True)
        self._right_motor.enableVoltageCompensation(12.0)
        self._encoder_right = self._right_motor.getEncoder()

        self._ref_rpm = 0.0
        self._reached_speed_left = False
        self._reached_speed_right = False

        if RobotBase.isSimulation():
            self.left_motor_sim = SparkMaxSim(self._left_motor)
            self.right_motor_sim = SparkMaxSim(self._right_motor)

    def shoot(self, rpm: float):
        left_volts, self._reached_speed_left = computeVoltage(
            rpm, self._encoder_left.getVelocity(), self.p_left, self.ff_left
        )
        right_volts, self._reached_speed_right = computeVoltage(
            rpm, self._encoder_right.getVelocity(), self.p_right, self.ff_right
        )

        self._left_motor.setVoltage(12)
        self._right_motor.setVoltage(12)

        self._ref_rpm = rpm

    def hasReachedSpeed(self):
        return self._reached_speed_left and self._reached_speed_right

    def stop(self):
        self._left_motor.stopMotor()
        self._right_motor.stopMotor()
        self._reached_speed_left = False
        self._reached_speed_right = False

    def simulationPeriodic(self):
        self.left_motor_sim.setVelocity(10000 * self._left_motor.get())
        self.right_motor_sim.setVelocity(10000 * self._left_motor.get())

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(_):
            pass

        builder.addBooleanProperty(
            "reached_speed_left", lambda: self._reached_speed_left, noop
        )
        builder.addBooleanProperty(
            "reached_speed_right", lambda: self._reached_speed_right, noop
        )
        builder.addFloatProperty("velocity_left", self._encoder_left.getVelocity, noop)
        builder.addFloatProperty(
            "velocity_right", self._encoder_right.getVelocity, noop
        )
        builder.addFloatProperty("ref_rpm", lambda: self._ref_rpm, noop)
