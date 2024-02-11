import wpilib
from wpilib import RobotBase
from wpilib.simulation import PWMSim, EncoderSim

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.switch import Switch


class Pivot(SafeSubsystem):
    speed_up = autoproperty(0.5)
    speed_down = autoproperty(-0.25)
    height_max = autoproperty(255.0)
    height_min = 0.0

    def __init__(self):
        super().__init__()

        self._switch_up = Switch(ports.pivot_switch_up, Switch.Type.NormallyClosed)
        self._switch_down = Switch(ports.pivot_switch_down, Switch.Type.NormallyClosed)
        self._motor = wpilib.VictorSP(ports.pivot_motor)
        self._encoder = wpilib.Encoder(ports.pivot_encoder_a, ports.pivot_encoder_b)

        self.offset = 0.0
        self._has_reset = False
        self._prev_is_down = False
        self._prev_is_up = False

        if RobotBase.isSimulation():
            self._sim_motor = PWMSim(self._motor)
            self._sim_encoder = EncoderSim(self._encoder)
            self._encoder.setDistancePerPulse(0.03)

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch_down.isPressed():
            self.offset = self.height_min - self._encoder.getDistance()
            self._has_reset = True
        self._prev_is_down = self._switch_down.isPressed()

        if self._prev_is_up and not self._switch_up.isPressed():
            self.offset = self.height_max - self._encoder.getDistance()
            self._has_reset = True
        self._prev_is_up = self._switch_up.isPressed()

    def simulationPeriodic(self) -> None:
        assert not (self.isUp() and self.isDown()), "Both switches are on at the same time which doesn't make any sense"
        # self._sim_encoder.setRate(self._motor.getSpeed())
        self._sim_encoder.setDistance(self._sim_encoder.getDistance() + self._motor.get())

        if self.getHeight() < self.height_min:
            self._switch_down.setSimPressed()
        else:
            self._switch_down.setSimUnpressed()

        if self.getHeight() > self.height_max:
            self._switch_up.setSimPressed()
        else:
            self._switch_up.setSimUnpressed()

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
        return self._switch_down.isPressed() or (self._has_reset and self.getHeight() < self.height_min)

    def isUp(self) -> bool:
        return self._switch_up.isPressed() or (self._has_reset and self.getHeight() > self.height_max)

    def stop(self):
        self._motor.stopMotor()

    def getHeight(self):
        return self._encoder.getDistance() + self.offset

    def getMotorInput(self):
        return self._motor.get()