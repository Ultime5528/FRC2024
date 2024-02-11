import rev
import wpilib
from wpilib import RobotBase

from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureLeader
from utils.switch import Switch


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.25)
    speed_down = autoproperty(-0.25)
    speed_unload = autoproperty(-0.1)

    stall_limit = autoproperty(15)
    free_limit = autoproperty(30)
    sim_max_height = 100

    ratchet_lock_angle = autoproperty(50.0)
    ratchet_unlock_angle = autoproperty(110.0)

    def __init__(self, port_motor, port_switch_up, port_switch_down, port_ratchet):
        super().__init__()
        self._motor = rev.CANSparkMax(port_motor, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(
            self._motor, "brake", stallLimit=self.stall_limit, freeLimit=self.free_limit
        )

        self._ratchet_servo = wpilib.Servo(port_ratchet)

        self._switch_up = Switch(port_switch_up, Switch.Type.NormallyClosed)
        self._switch_down = Switch(port_switch_down, Switch.Type.NormallyClosed)

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
        self._motor.set(self.speed_unload)

    def stop(self):
        self._motor.set(0)

    def isUp(self):
        return self._switch_up.isPressed()

    def isDown(self):
        return self._switch_down.isPressed()

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
