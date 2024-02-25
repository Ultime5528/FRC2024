from abc import abstractmethod, ABC

import rev
import wpilib
from wpilib import RobotBase
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureLeader
from utils.switch import Switch


class ClimberProperties(ABC):
    @property
    @abstractmethod
    def port_motor(self) -> int: ...
    @property
    @abstractmethod
    def port_switch_up(self) -> int: ...
    @property
    @abstractmethod
    def port_switch_down(self) -> int: ...
    @property
    @abstractmethod
    def port_ratchet(self) -> int: ...
    @property
    @abstractmethod
    def ratchet_lock_angle(self) -> float: ...
    @property
    @abstractmethod
    def ratchet_unlock_angle(self) -> float: ...
    @property
    @abstractmethod
    def height_max(self) -> float: ...
    @property
    @abstractmethod
    def height_min(self) -> float: ...
    @property
    @abstractmethod
    def inversed(self) -> bool: ...


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.6)
    speed_down = autoproperty(-0.6)
    speed_unload = autoproperty(-0.1)

    sim_max_height = 100.0

    stall_limit = autoproperty(15)
    free_limit = autoproperty(30)

    def __init__(self, properties: ClimberProperties):
        super().__init__()
        self._motor = rev.CANSparkMax(
            properties.port_motor, rev.CANSparkMax.MotorType.kBrushless
        )
        configureLeader(self._motor, "brake", inverted=properties.inversed)
        self._encoder = self._motor.getEncoder()

        self._ratchet_servo = wpilib.Servo(properties.port_ratchet)
        self.addChild("servo", self._ratchet_servo)

        self._switch_up = Switch(Switch.Type.NormallyClosed, properties.port_switch_up)
        self._switch_down = Switch(Switch.Type.AlwaysUnpressed)

        self.properties = properties

        self._prev_is_up = False
        self._has_reset = False
        self._offset = 0.0

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor)

    def extend(self):
        if not self.isUp():
            self._motor.set(self.speed_up)
        else:
            self.stop()

    def retract(self):
        if not self.isDown():
            self._motor.set(self.speed_down)
        else:
            self.stop()

    def unload(self):
        # Bypass security during unload
        self._motor.set(self.speed_unload)

    def stop(self):
        self._motor.stopMotor()

    def isUp(self):
        return (
            self._switch_up.isPressed()
            or self._has_reset
            and self.getHeight() > self.properties.height_max
        )

    def isDown(self):
        return (
            self._switch_down.isPressed()
            or self.getHeight() < self.properties.height_min
        )

    def periodic(self) -> None:
        if self._prev_is_up and not self._switch_up.isPressed():
            self.setHeight(self.properties.height_max)

        self._prev_is_up = self._switch_up.isPressed()

    def setHeight(self, reset_value):
        self._offset = reset_value - self._encoder.getPosition()
        self._has_reset = True

    def getHeight(self):
        return self._encoder.getPosition() + self._offset

    def getMotorSpeed(self):
        return self._motor.get()

    def lockRatchet(self):
        self._ratchet_servo.set(self.properties.ratchet_lock_angle)

    def unlockRatchet(self):
        self._ratchet_servo.set(self.properties.ratchet_unlock_angle)

    def simulationPeriodic(self) -> None:
        self._sim_motor.setVelocity(self._motor.get())
        self._sim_motor.setPosition(self._sim_motor.getPosition() + self._motor.get())

        if self._sim_motor.getPosition() > 0:
            self._switch_down.setSimUnpressed()
        else:
            self._switch_down.setSimPressed()

        if self._sim_motor.getPosition() < self.sim_max_height:
            self._switch_up.setSimUnpressed()
        else:
            self._switch_up.setSimPressed()

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("motor_amps", self._motor.getOutputCurrent, noop)
        builder.addFloatProperty("encoder", self._encoder.getPosition, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addFloatProperty("height", self.getHeight, noop)
        builder.addFloatProperty("servo", self._ratchet_servo.get, noop)
        builder.addBooleanProperty("switch_up", self._switch_up.isPressed, noop)
        builder.addBooleanProperty("switch_down", self._switch_down.isPressed, noop)
        builder.addBooleanProperty("isUp", self.isUp, noop)
        builder.addBooleanProperty("isDown", self.isDown, noop)


class ClimberLeftProperties(ClimberProperties):
    port_motor = ports.climber_motor_left
    port_switch_up = ports.climber_left_switch_up
    port_switch_down = ports.climber_left_switch_down
    port_ratchet = ports.climber_servo_left
    ratchet_lock_angle = autoproperty(1.0, subtable="ClimberLeft")
    ratchet_unlock_angle = autoproperty(0.05, subtable="ClimberLeft")
    height_max = autoproperty(222.0, subtable="ClimberLeft")
    height_min = autoproperty(20, subtable="ClimberLeft")
    inversed = False


climber_left_properties = ClimberLeftProperties()


class ClimberRightProperties(ClimberProperties):
    port_motor = ports.climber_motor_right
    port_switch_up = ports.climber_right_switch_up
    port_switch_down = ports.climber_right_switch_down
    port_ratchet = ports.climber_servo_right
    ratchet_lock_angle = autoproperty(0.3, subtable="ClimberRight")
    ratchet_unlock_angle = autoproperty(0.85, subtable="ClimberRight")
    height_max = autoproperty(222.0, subtable="ClimberRight")
    height_min = autoproperty(20, subtable="ClimberRight")
    inversed = True


climber_right_properties = ClimberRightProperties()
