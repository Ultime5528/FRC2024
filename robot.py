#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib

from commands.climber.extendclimber import ExtendClimber
from commands.climber.forceresetclimber import ForceResetClimber
from commands.climber.lockratchet import LockRatchet
from commands.climber.retractclimber import RetractClimber
from commands.climber.unlockratchet import UnlockRatchet
from commands.drivetrain.drive import DriveField, Drive
from commands.intake.drop import Drop
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.pivot.forceresetpivot import ForceResetPivot
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.pivot.resetpivotup import ResetPivotUp
from subsystems.climber import Climber
from subsystems.climber import climber_left_properties, climber_right_properties
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.pivot import Pivot


class Robot(commands2.TimedCommandRobot):
    def robotInit(self):
        # robotInit fonctionne mieux avec les tests que __init__.

        wpilib.LiveWindow.enableAllTelemetry()
        wpilib.DriverStation.silenceJoystickConnectionWarning(True)
        self.enableLiveWindowInTest(True)

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
        self.climber_left = Climber(climber_left_properties)
        self.climber_right = Climber(climber_right_properties)
        self.intake = Intake()
        self.pivot = Pivot()

        """
        Default subsystem commands
        """
        self.drivetrain.setDefaultCommand(
            DriveField(self.drivetrain, self.xbox_controller)
        )

        """
        Setups
        """
        self.setupAuto()
        self.setupButtons()
        self.setupSubsystemOnDashboard()
        self.setupCommandsOnDashboard()

    def setupAuto(self):
        self.auto_chooser.setDefaultOption("Nothing", None)
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        pass

    def setupSubsystemOnDashboard(self):
        wpilib.SmartDashboard.putData("Drivetrain", self.drivetrain)
        wpilib.SmartDashboard.putData("ClimberLeft", self.climber_left)
        wpilib.SmartDashboard.putData("ClimberRight", self.climber_right)
        wpilib.SmartDashboard.putData("Intake", self.intake)
        wpilib.SmartDashboard.putData("Pivot", self.pivot)

    def setupCommandsOnDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard(
            "Drivetrain", DriveField(self.drivetrain, self.xbox_controller)
        )
        putCommandOnDashboard(
            "Drivetrain", Drive(self.drivetrain, self.xbox_controller)
        )

        for climber, name in (
            (self.climber_left, "Left"),
            (self.climber_right, "Right"),
        ):
            putCommandOnDashboard(
                "Climber" + name,
                ExtendClimber(climber),
                "ExtendClimber." + name,
            )
            putCommandOnDashboard(
                "Climber" + name,
                RetractClimber(climber),
                "RetractClimber." + name,
            )
            putCommandOnDashboard(
                "Climber" + name,
                ForceResetClimber.toMin(climber),
                "ForceResetClimber.toMin." + name,
            )
            putCommandOnDashboard(
                "Climber" + name,
                ForceResetClimber.toMax(climber),
                "ForceResetClimber.toMax." + name,
            )
            putCommandOnDashboard(
                "Climber" + name, LockRatchet(climber), "LockRatchet." + name
            )
            putCommandOnDashboard(
                "Climber" + name, UnlockRatchet(climber), "UnlockRatchet." + name
            )

        putCommandOnDashboard("Intake", Drop(self.intake))
        putCommandOnDashboard("Intake", PickUp(self.intake))
        putCommandOnDashboard("Intake", Load(self.intake))

        putCommandOnDashboard("Pivot", MovePivot.toAmp(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerFar(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerClose(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toLoading(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotDown(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotUp(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMin(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMax(self.pivot))

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def teleopInit(self):
        self.drivetrain.resetGyro()
        if self.auto_command:
            self.auto_command.cancel()


def putCommandOnDashboard(
    sub_table: str, cmd: commands2.Command, name: str = None
) -> commands2.Command:
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
