import rev
import wpilib
import ports

from wpilib import RobotBase
from wpilib.simulation import DIOSim

from utils.asserthelper import implies
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim


class Climber(SafeSubsystem):
    speed_up = autoproperty(0.25)
    speed_down = autoproperty(-0.25)
    sim_min_height = autoproperty(0.0)
    sim_max_height = autoproperty(100.0)

    def __init__(self, port_motor, port_switch_up, port_switch_down) -> None:
        super().__init__()

        assert ports.can_min <= port_motor <= ports.can_max
        assert ports.dio_min <= port_switch_up <= ports.dio_max
        assert ports.dio_min <= port_switch_down <= ports.dio_max
        assert port_switch_up != port_switch_down

        self._motor = rev.CANSparkMax(port_motor,
                                      rev.CANSparkMax.MotorType.kBrushless)

        self._switch_up = wpilib.DigitalInput(port_switch_up)
        self._switch_down = wpilib.DigitalInput(port_switch_down)

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor)
            self._sim_switch_up = DIOSim(self._switch_up)
            self._sim_switch_down = DIOSim(self._switch_down)

            if self._sim_motor.getPosition() <= self.sim_min_height:
                self._sim_switch_down.setValue(True)
            else:
                self._sim_switch_down.setValue(False)

            if self._sim_motor.getPosition() <= self.sim_max_height:
                self._sim_switch_up.setValue(True)
            else:
                self._sim_switch_up.setValue(False)

        assert self.checkInvariants()

    def extend(self) -> None:
        assert self.checkInvariants()
        if not self.isUp():
            self._motor.set(self.speed_up)
        else:
            self.stop()
        assert self.checkInvariants()


    def retract(self) -> None:
        assert self.checkInvariants()
        if not self.isDown():
            self._motor.set(self.speed_down)
        else:
            self.stop()
        assert self.checkInvariants()


    def stop(self) -> None:
        assert self.checkInvariants()
        self._motor.set(0.0)
        assert self.checkInvariants()


    def isUp(self) -> bool:
        assert self.checkInvariants()
        return not self._switch_up.get()

    def isDown(self) -> bool:
        assert self.checkInvariants()
        return not self._switch_down.get()

    def simulationPeriodic(self) -> None:
        assert self.checkInvariants()
        self._sim_motor.setVelocity(self._motor.get())
        assert self.checkInvariants()

    def periodic(self) -> None:
        assert self.checkInvariants()

    def checkInvariants(self) -> bool:
        assert self._motor
        assert self._switch_up
        assert self._switch_down

        if RobotBase.isSimulation():
            assert self._sim_motor
            assert self._sim_switch_up
            assert self._sim_switch_down

        assert self.speed_up > 0.0
        assert self.speed_down < 0.0
        assert self.sim_min_height < self.sim_max_height

        assert self._motor.getMotorType() == rev.CANSparkMax.MotorType.kBrushless
        assert ports.dio_min <= self._switch_up.getChannel() <= ports.dio_max
        assert ports.dio_min <= self._switch_down.getChannel() <= ports.dio_max
        assert self._switch_down.getChannel() == self._switch_up.getChannel() + 2

        assert 0.0 <= self._motor.get() <= self.speed_up

        assert implies(self._switch_up.get(), self._motor.get() == 0.0)
        assert implies(self._switch_down.get(), self._motor.get() == 0.0)
        assert implies(self._motor.get() > 0.0, not self._switch_up.get())
        assert implies(self._motor.get() < 0.0, not self._switch_down.get())

        return True