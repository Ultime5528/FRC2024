import wpilib
import phoenix5
from wpilib import RobotBase
from wpilib.simulation import DIOSim
from utils.switch import Switch
from utils.switch import Type
import ports
from utils.safesubsystem import SafeSubsystem
from utils.property import autoproperty


class Pivot(SafeSubsystem):
    speed_up = autoproperty(0.5)
    speed_down = autoproperty(-0.25)

    def __init__(self):
        super().__init__()

        self._switch_up = Switch(ports.pivot_switch_up, Switch.Type.NormallyOpen)
        self._switch_down = Switch(ports.pivot_switch_down, Switch.Type.NormallyOpen)
        self._motor = wpilib.PWMVictorSPX(ports.pivot_motor)
        self._encoder = wpilib.Encoder(ports.pivot_encoder_a, ports.pivot_encoder_b)

    def simulationPeriodic(self) -> None:
        assert self.checkInvariants()

    def moveUp(self):
        self.setSpeed(self.speed_up)

    def moveDown(self):
        self.setSpeed(self.speed_down)

    def setSpeed(self, speed: float):
        assert -1.0 <= speed <= 1.0

        if self.isDown():
            self._motor.set(speed if speed >= 0 else 0)
        elif self.isUp():
            self._motor.set(speed if speed <= 0 else 0)
        else:
            self._motor.set(speed)

    def isDown(self) -> bool:
        return self._switch_down.isPressed()

    def isUp(self) -> bool:
        return self._switch_up.isPressed()

    def stop(self):
        self._motor.stopMotor()

    def resetEncoder(self):
        self._encoder.reset()

    def getPosition(self):
        return self._encoder.get()

    def getMotorInput(self):
        return self._motor.get()

    def checkInvariants(self) -> bool:
        assert not (self.isUp() and self.isDown()), "Both switches are on at the same time which doesn't make any sense"
        return True
