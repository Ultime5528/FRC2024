#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib

import ports
from commands.drivetrain.drive import DriveField, Drive
from subsystems.drivetrain import Drivetrain
from subsystems.climber import Climber
from commands.climber.extendclimber import ExtendClimber
from commands.climber.retractclimber import RetractClimber


class Robot(commands2.TimedCommandRobot):
    def __init__(self):
        super().__init__()
        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)

        """
        Autonomous
        """
        self.auto_command: Optional[commands2.Command] = None
        self.auto_chooser = wpilib.SendableChooser()

        """
        Joysticks
        """
        self.xbox_controller = commands2.button.CommandXboxController(0)

        """
        Subsystems
        """
        self.drivetrain = Drivetrain(self.getPeriod())
        self.climber_left = Climber(
            ports.climber_motor_left,
            ports.climber_switch_up_left,
            ports.climber_switch_down_left
        )
        self.climber_right = Climber(
             ports.climber_motor_right,
             ports.climber_switch_up_right,
             ports.climber_switch_down_right
        )




        """
        Default subsystem commands
        """
        self.drivetrain.setDefaultCommand(DriveField(self.drivetrain, self.xbox_controller))

        """
        Setups
        """
        self.setupAuto()
        self.setupButtons()
        self.setupDashboard()

    def setupAuto(self):
        self.auto_chooser.setDefaultOption("Nothing", None)
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        pass
    
    def setupDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard("Drivetrain", DriveField(self.drivetrain, self.xbox_controller))
        putCommandOnDashboard("Drivetrain", Drive(self.drivetrain, self.xbox_controller))
        putCommandOnDashboard("Climber", ExtendClimber(self.climber_left), "ExtendClimber.left")
        putCommandOnDashboard("Climber", RetractClimber(self.climber_left), "RetractClimber.left")
        putCommandOnDashboard("Climber", ExtendClimber(self.climber_right), "ExtendClimber.right")
        putCommandOnDashboard("Climber", RetractClimber(self.climber_right), "RetractClimber.right")



    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def teleopInit(self):
        self.drivetrain.resetGyro()
        if self.auto_command:
            self.auto_command.cancel()


def putCommandOnDashboard(sub_table: str, cmd: commands2.Command, name: str = None) -> commands2.Command:
    if sub_table:
        sub_table += "/"
    else:
        sub_table = ""

    if name is None:
        name = cmd.getName()
    else:
        cmd.setName(name)

    wpilib.SmartDashboard.putData(sub_table + name, cmd)

    return cmd


if __name__ == "__main__":
    wpilib.run(Robot)
