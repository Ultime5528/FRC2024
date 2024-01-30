
import rev
import wpilib
from wpilib import RobotBase

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim


class Intake(SafeSubsystem):
    speed_in = autoproperty(0.3)
    speed_out = autoproperty(-0.17)

    def __init__(self):
        super().__init__()
        self._motor = rev.CANSparkMax(ports.intake_motor, rev.CANSparkMax.MotorType.kBrushless)
        self._sensor = wpilib.DigitalInput(ports.intake_sensor)

        if RobotBase.isSimulation():
            self.sim_motor = SparkMaxSim(self._motor)

    def pickUp(self):
        self._motor.set(self.speed_in)

    def drop(self):
        self._motor.set(self.speed_out)

    def stop(self):
        self._motor.stopMotor()

    def hasNote(self):
        return self._sensor.get()

    def simulationPeriodic(self) -> None:
        self.sim_motor.setVelocity(self._motor.get())
        self.sim_motor.setPosition(self.sim_motor.getPosition() + self._motor.get())
