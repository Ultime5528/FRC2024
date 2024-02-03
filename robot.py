#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib

from commands.auto.drivesquares import DriveSquares
from commands.drive import DriveField, Drive
from commands.pivot.movepivot import MovePivot
from subsystems.drivetrain import Drivetrain
from subsystems.pivot import Pivot
from utils.switch import Switch


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
        #self.shooter = Shooter()
        self.pivot = Pivot()

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
        self.xbox_controller.button(1).onTrue(DriveSquares(self.drivetrain))

    def setupDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard("Drivetrain", DriveField(self.drivetrain, self.xbox_controller))
        putCommandOnDashboard("Drivetrain", Drive(self.drivetrain, self.xbox_controller))
        putCommandOnDashboard("Pivot", MovePivot(self.pivot, self.xbox_controller))

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
