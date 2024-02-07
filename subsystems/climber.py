import rev
import wpilib

from wpilib import RobotBase
from wpilib.simulation import DIOSim

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.sparkmaxutils import configureLeader
from utils.switch import Switch


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.25)
    speed_down = autoproperty(-0.25)
    stall_limit = autoproperty(15)
    free_limit = autoproperty(30)
    sim_max_height = 100
    height_max = autoproperty(100.0)
    height_min = autoproperty(0.0)

    def __init__(self, port_motor, port_switch_up, port_switch_down):
        super().__init__()
        self._motor = rev.CANSparkMax(port_motor, rev.CANSparkMax.MotorType.kBrushless)
        configureLeader(
            self._motor, "brake", stallLimit=self.stall_limit, freeLimit=self.free_limit
        )
        self._encoder = self._motor.getEncoder()

        self._switch_up = Switch(port_switch_up, Switch.Type.NormallyOpen)
        self._switch_down = Switch(port_switch_down, Switch.Type.NormallyOpen)

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

    def stop(self):
        self._motor.set(0)

    def isUp(self):


        return self._switch_up.isPressed() or self._encoder.getPosition() >= self.height_max

    def isDown(self):
        return self._switch_down.isPressed() or self._encoder.getPosition() <= self.height_min

    def periodic(self) -> None:
        if self._prev_is_up and not self._switch_up.isPressed():
            self._offset = self.height_max - self._encoder.getPosition()

        self._prev_is_up = self._switch_up.isPressed()

    def getHeight(self):
        return self._encoder.getPosition() + self._offset

    def getMotorSpeed(self):
        return self._motor.get()

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
