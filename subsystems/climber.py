import rev
import wpilib

from wpilib import RobotBase
from wpilib.simulation import DIOSim

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem
from utils.sparkmaxsim import SparkMaxSim


class Climber(SafeSubsystem):
    climber_speed_up = autoproperty(0.25)
    climber_speed_down = autoproperty(-0.25)

    def __init__(self, port_motor, portswitchup, portswitchdown):
        super().__init__()
        self.motor = rev.CANSparkMax(port_motor,
                                     rev.CANSparkMax.MotorType.kBrushless)

        self.switch_up = wpilib.DigitalInput(portswitchup)
        self.switch_down = wpilib.DigitalInput(portswitchdown)

        if RobotBase.isSimulation():
            self.motor_sim = SparkMaxSim(self.motor)
            self.sim_switch_up = DIOSim(self.switch_up)
            self.sim_switch_down = DIOSim(self.switch_down)


    def extend(self):
        if not self.isUp():
            self.motor.set(self.climber_speed_up)
        else:
            self.stop()

    def retract(self):
        if not self.isDown():
            self.motor.set(self.climber_speed_down)
        else:
            self.stop()

    def stop(self):
        self.motor.set(0)

    def isUp(self):
        return not self.switch_up.get()

    def isDown(self):
        return not self.switch_down.get()

    def simulationPeriodic(self) -> None:
        self.motor_sim.setVelocity(self.motor.get())

