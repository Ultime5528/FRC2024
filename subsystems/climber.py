import rev
import wpilib
from wpilib import RobotBase
from wpiutil import SendableBuilder

from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureLeader
from utils.switch import Switch


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.25)
    speed_down = autoproperty(-0.25)
    speed_unload = autoproperty(-0.1)

    height_min = 0.0
    height_max = autoproperty(100.0)
    sim_max_height = 100.0

    stall_limit = autoproperty(15)
    free_limit = autoproperty(30)

    ratchet_lock_angle = autoproperty(50.0)
    ratchet_unlock_angle = autoproperty(110.0)

    def __init__(self, port_motor, port_switch_up, port_switch_down, port_ratchet):
        super().__init__()
        self._motor = rev.CANSparkMax(port_motor, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(
            self._motor, "brake", stallLimit=self.stall_limit, freeLimit=self.free_limit
        )
        self._encoder = self._motor.getEncoder()

        self._ratchet_servo = wpilib.Servo(port_ratchet)

        self._switch_up = Switch(port_switch_up, Switch.Type.NormallyClosed)
        self._switch_down = Switch(port_switch_down, Switch.Type.NormallyClosed)

        self._prev_is_up = False
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
        self._motor.set(0)

    def isUp(self):
        return (
            self._switch_up.isPressed() or self._encoder.getPosition() > self.height_max
        )

    def isDown(self):
        return (
            self._switch_down.isPressed()
            or self._encoder.getPosition() < self.height_min
        )

    def periodic(self) -> None:
        if self._prev_is_up and not self._switch_up.isPressed():
            self.setHeight(self.height_max)

        self._prev_is_up = self._switch_up.isPressed()

    def setHeight(self, reset_value):
        self._offset = reset_value - self._encoder.getPosition()

    def getHeight(self):
        return self._encoder.getPosition() + self._offset

    def getMotorSpeed(self):
        return self._motor.get()

    def lockRatchet(self):
        self._ratchet_servo.setAngle(self.ratchet_lock_angle)

    def unlockRatchet(self):
        self._ratchet_servo.setAngle(self.ratchet_unlock_angle)

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

        builder.addFloatProperty(
            "encoder_value", self._encoder.getPosition, lambda x: None
        )
        builder.addFloatProperty(
            "offset", lambda: self._offset, lambda x: setOffset(x)
        )
        builder.addFloatProperty("height", self.getHeight, lambda x: None)
