import rev
from wpilib import RobotBase
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim
from utils.switch import Switch


class Intake(SafeSubsystem):
    speed_in = autoproperty(0.3)
    speed_load = autoproperty(0.8)
    speed_out = autoproperty(-0.17)

    def __init__(self):
        super().__init__()
        self._motor = rev.CANSparkMax(
            ports.intake_motor, rev.CANSparkMax.MotorType.kBrushless
        )
        self._sensor = Switch(ports.intake_sensor, Switch.Type.NormallyOpen)

        if RobotBase.isSimulation():
            self._sim_motor = SparkMaxSim(self._motor)

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

    def simulationPeriodic(self) -> None:
        self._sim_motor.setVelocity(self._motor.get())
        self._sim_motor.setPosition(self._sim_motor.getPosition() + self._motor.get())

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)

        builder.addBooleanProperty("hasNote", self.hasNote, lambda x: None)
