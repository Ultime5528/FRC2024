import rev
import wpilib

from wpilib import RobotBase
from wpilib.simulation import DIOSim

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.25)
    speed_down = autoproperty(-0.25)
    _sim_max_height = 100

    def __init__(self, port_motor, port_switch_up, port_switch_down):
        super().__init__()
        self._motor = rev.CANSparkMax(port_motor,
                                      rev.CANSparkMax.MotorType.kBrushless)

        self._switch_up = wpilib.DigitalInput(port_switch_up)
        self._switch_down = wpilib.DigitalInput(port_switch_down)

        if RobotBase.isSimulation():
            self.sim_motor = SparkMaxSim(self._motor)
            self.sim_switch_up = DIOSim(self._switch_up)
            self.sim_switch_down = DIOSim(self._switch_down)

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
        return not self._switch_up.get()

    def isDown(self):
        return not self._switch_down.get()

    def simulationPeriodic(self) -> None:
        self.sim_motor.setVelocity(self._motor.get())
        self.sim_motor.setPosition(self.sim_motor.getPosition() + self._motor.get())

        if self.sim_motor.getPosition() >= 0:
            self.sim_switch_down.setValue(True)
        else:
            self.sim_switch_down.setValue(False)

        if self.sim_motor.getPosition() <= self._sim_max_height:
            self.sim_switch_up.setValue(True)
        else:
            self.sim_switch_up.setValue(False)
