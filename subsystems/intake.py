import wpilib
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.switch import Switch


class Intake(SafeSubsystem):
    speed_in = autoproperty(0.75)
    speed_load = autoproperty(0.75)
    speed_out = autoproperty(-0.75)

    def __init__(self):
        super().__init__()

        self._motor = wpilib.VictorSP(ports.intake_motor)

        self._sensor = Switch(Switch.Type.NormallyOpen, ports.intake_sensor)

    def pickUp(self):
        self._motor.set(self.speed_in)

    def load(self):
        self._motor.set(self.speed_load)

    def drop(self):
        self._motor.set(self.speed_out)

    def stop(self):
        self._motor.stopMotor()

    def hasNote(self):
        return self._sensor.isPressed()

    # def simulationPeriodic(self) -> None:
    #     self._sim_motor.setVelocity(self._motor.get())
    #     self._sim_motor.setPosition(self._sim_motor.getPosition() + self._motor.get())

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        def noop(x):
            pass

        builder.addFloatProperty("motor_input", self._motor.get, noop)
        builder.addBooleanProperty("hasNote", self.hasNote, noop)
