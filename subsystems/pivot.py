from enum import Enum, auto
from typing import Union

import wpilib
from wpilib import RobotBase
from wpilib.simulation import PWMSim, EncoderSim
from wpiutil import SendableBuilder

import ports
from utils.linearinterpolator import LinearInterpolator
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.switch import Switch

# X is height in camera view, y is the subsequent wanted pivot pitch
interpolation_points = [(10, 20), (20, 40)]

class Pivot(SafeSubsystem):
    class State(Enum):
        Invalid = auto()
        Moving = auto()
        Loading = auto()
        SpeakerClose = auto()
        SpeakerFar = auto()
        Amp = auto()
        LockedInterpolation = auto()

    speed_up = autoproperty(0.2)
    speed_down = autoproperty(-0.75)
    speed_maintain = autoproperty(-0.2)
    height_min = 0.0
    height_max = autoproperty(55.0)

    def __init__(self):
        super().__init__()
        self._switch_up = Switch(Switch.Type.NormallyClosed, ports.pivot_switch_up)
        self._switch_down = Switch(Switch.Type.NormallyClosed, ports.pivot_switch_down)
        self._motor = wpilib.VictorSP(ports.pivot_motor)
        self._encoder = wpilib.Encoder(
            ports.pivot_encoder_a, ports.pivot_encoder_b, reverseDirection=True
        )
        self.addChild("motor", self._motor)
        self.addChild("encoder", self._encoder)

        self._interpolator = LinearInterpolator(interpolation_points)
        self._offset = 0.0
        self._has_reset = False
        self._prev_is_down = False
        self._prev_is_up = False
        self.state = Pivot.State.Invalid

        if RobotBase.isSimulation():
            self._sim_motor = PWMSim(self._motor)
            self._sim_encoder = EncoderSim(self._encoder)
            self._encoder.setDistancePerPulse(0.03)

    def periodic(self) -> None:
        if self._prev_is_down and not self._switch_down.isPressed():
            self._offset = self.height_min - self._encoder.getDistance()
            self._has_reset = True
        self._prev_is_down = self._switch_down.isPressed()

        # if self._prev_is_up and not self._switch_up.isPressed():
        #     self._offset = self.height_max - self._encoder.getDistance()
        #     self._has_reset = True
        # self._prev_is_up = self._switch_up.isPressed()

    def simulationPeriodic(self) -> None:
        assert not (
            self.isUp() and self.isDown()
        ), "Both switches are on at the same time which doesn't make any sense"

        self._sim_encoder.setDistance(
            self._sim_encoder.getDistance() + self._motor.get()
        )

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

    def maintain(self):
        self.setSpeed(self.speed_maintain)

    def getInterpolatedPosition(self, target_pitch: float) -> float:
        return self._interpolator.interpolate(target_pitch)

    def isDown(self) -> bool:
        return self._switch_down.isPressed()

    def isUp(self) -> bool:
        # return self._switch_up.isPressed() or (
        #     self._has_reset and self.getHeight() > self.height_max
        # )
        return self._has_reset and self.getHeight() > self.height_max

    def stop(self):
        self._motor.stopMotor()

    def setHeight(self, reset_value):
        self._offset = reset_value - self._encoder.getDistance()

    def getHeight(self):
        return self._encoder.getDistance() + self._offset

    def getMotorInput(self):
        return self._motor.get()

    def hasReset(self):
        return self._has_reset

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def setOffset(value: float):
            self._offset = value

        def noop(x):
            pass

        def setHasReset(value: bool):
            self._has_reset = value

        builder.addStringProperty("state", lambda: self.state.name, noop)
        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addFloatProperty("encoder", self._encoder.getDistance, noop)
        builder.addFloatProperty("offset", lambda: self._offset, lambda x: setOffset(x))
        builder.addFloatProperty("height", self.getHeight, noop)
        builder.addBooleanProperty("has_reset", lambda: self._has_reset, setHasReset)
        builder.addBooleanProperty("switch_up", self._switch_up.isPressed, noop)
        builder.addBooleanProperty("switch_down", self._switch_down.isPressed, noop)
        builder.addBooleanProperty("isUp", self.isUp, noop)
        builder.addBooleanProperty("isDown", self.isDown, noop)
