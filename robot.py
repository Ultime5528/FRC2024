#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib
from wpimath.geometry import Pose2d, Rotation2d

from commands.aligneverything import AlignEverything
from commands.auto.autospeakercentershootline import AutoSpeakerCenterShootLine
from commands.auto.autospeakercentershoottwiceline import AutoSpeakerCenterShootTwiceLine
from commands.auto.autospeakerleftshootline import AutoSpeakerLeftShootLine
from commands.auto.autospeakerleftshoottwiceline import AutoSpeakerLeftShootTwiceLine
from commands.auto.autospeakerrightshootline import AutoSpeakerRightShootLine
from commands.auto.autospeakerrightshoottwiceline import AutoSpeakerRightShootTwiceLine
from commands.auto.megamodeautonome import MegaModeAutonome
from commands.climber.extendclimber import ExtendClimber
from commands.climber.forceresetclimber import ForceResetClimber
from commands.climber.lockratchet import LockRatchet
from commands.climber.retractclimber import RetractClimber
from commands.climber.unlockratchet import UnlockRatchet
from commands.drivetoposes import DriveToPoses
from commands.drivetrain.drive import DriveField, Drive
from commands.drivetrain.resetgyro import ResetGyro
from commands.intake.drop import Drop
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.led.lightall import LightAll
from commands.pivot.forceresetpivot import ForceResetPivot
from commands.pivot.maintainpivot import MaintainPivot
from commands.pivot.movepivot import MovePivot
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.pivot.resetpivotup import ResetPivotUp
from commands.shooter.manualshoot import ManualShoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import ShootAndMovePivotLoading
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.climber import Climber
from subsystems.climber import climber_left_properties, climber_right_properties
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.led import LEDController
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.vision import Vision
from utils.axistrigger import AxisTrigger


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
        self.panel_1 = commands2.button.CommandJoystick(1)
        self.panel_2 = commands2.button.CommandJoystick(2)

        """
        Subsystems
        """
        self.drivetrain = Drivetrain(self.getPeriod())
        self.climber_left = Climber(climber_left_properties)
        self.climber_right = Climber(climber_right_properties)
        self.intake = Intake()
        self.pivot = Pivot()
        self.shooter = Shooter()
        self.vision = Vision()
        self.led = LEDController()

        """
        Default subsystem commands
        """
        self.drivetrain.setDefaultCommand(
            DriveField(self.drivetrain, self.xbox_controller)
        )
        self.pivot.setDefaultCommand(MaintainPivot(self.pivot))

        """
        Setups
        """
        self.setupAuto()
        self.setupButtons()
        self.setupSubsystemOnDashboard()
        self.setupCommandsOnDashboard()

    def setupAuto(self):
        self.auto_chooser.setDefaultOption("Nothing", None)
        self.auto_chooser.addOption(
            "AutoSpeakerCenterShootLine",
            AutoSpeakerCenterShootLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "AutoSpeakerCenterShootTwiceLine",
            AutoSpeakerCenterShootTwiceLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "AutoSpeakerLeftShootLine",
            AutoSpeakerLeftShootLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "AutoSpeakerLeftShootTwiveLine",
            AutoSpeakerLeftShootTwiceLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "AutoSpeakerRightShootLine",
            AutoSpeakerRightShootLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "AutoSpeakerRightShootTwiceLine",
            AutoSpeakerRightShootTwiceLine(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        self.auto_chooser.addOption(
            "MegaModeAutonome",
            MegaModeAutonome(
                self.drivetrain, self.shooter, self.pivot, self.intake
            ),
        )
        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        self.xbox_controller.rightTrigger().whileTrue(
            AlignEverything(
                self.drivetrain, self.pivot, self.vision, self.xbox_controller
            )
        )
        self.xbox_controller.leftTrigger().whileTrue(
            AlignWithTag2D.toSpeaker(self.drivetrain, self.vision, self.xbox_controller)
        )

        # Copilot's panel
        AxisTrigger(self.panel_1, 1, "down").whileTrue(ExtendClimber(self.climber_left))
        AxisTrigger(self.panel_1, 1, "up").whileTrue(RetractClimber(self.climber_left))
        self.panel_1.button(3).onTrue(PickUp(self.intake))
        self.panel_1.button(2).onTrue(Drop(self.intake))
        self.panel_1.button(1).onTrue(MovePivot.toSpeakerClose(self.pivot))

        AxisTrigger(self.panel_2, 1, "down").whileTrue(
            ExtendClimber(self.climber_right)
        )
        AxisTrigger(self.panel_2, 1, "up").whileTrue(RetractClimber(self.climber_right))
        self.panel_2.button(2).onTrue(MovePivot.toSpeakerFar(self.pivot))
        self.panel_2.button(5).onTrue(
            ShootAndMovePivotLoading(self.shooter, self.pivot, self.intake)
        )
        self.panel_2.button(4).onTrue(ResetPivotDown(self.pivot))

    def setupSubsystemOnDashboard(self):
        wpilib.SmartDashboard.putData("Drivetrain", self.drivetrain)
        wpilib.SmartDashboard.putData("ClimberLeft", self.climber_left)
        wpilib.SmartDashboard.putData("ClimberRight", self.climber_right)
        wpilib.SmartDashboard.putData("Intake", self.intake)
        wpilib.SmartDashboard.putData("Pivot", self.pivot)
        wpilib.SmartDashboard.putData("Shooter", self.shooter)
        wpilib.SmartDashboard.putData("Vision", self.vision)
        wpilib.SmartDashboard.putData("LED", self.led)

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
        putCommandOnDashboard(
            "Drivetrain",
            AlignWithTag2D.toSpeaker(
                self.drivetrain, self.vision, self.xbox_controller
            ),
        )

        putCommandOnDashboard("Drivetrain", ResetGyro(self.drivetrain))

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

        putCommandOnDashboard("LED", LightAll(self.led))

        putCommandOnDashboard("Pivot", MovePivot.toAmp(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerFar(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerClose(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toLoading(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotDown(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotUp(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMin(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMax(self.pivot))
        putCommandOnDashboard("Pivot", MovePivotContinuous(self.pivot, self.vision))
        putCommandOnDashboard(
            "Drivetrain",
            DriveToPoses(
                self.drivetrain,
                Pose2d(15.20, 5.55, Rotation2d.fromDegrees(180)),
                [Pose2d(14, 5.55, Rotation2d.fromDegrees(180))]
            ),
            "Centre",
        )
        putCommandOnDashboard(
            "Drivetrain",
            DriveToPoses(self.drivetrain,
                         Pose2d(16.08-0.22, 6.33+0.385, Rotation2d.fromDegrees(120)),
                         [Pose2d(15, 7, Rotation2d.fromDegrees(120)),
                        Pose2d(14, 7, Rotation2d.fromDegrees(180))]),
            "Left",
        )
        putCommandOnDashboard(
            "Drivetrain",
            DriveToPoses(self.drivetrain,
                         Pose2d(16.08 - 0.22, 6.33 + 0.385, Rotation2d.fromDegrees(120)),
                         [Pose2d(15, 7, Rotation2d.fromDegrees(120)),
                          Pose2d(15, 7, Rotation2d.fromDegrees(180)),
                          Pose2d(14, 7, Rotation2d.fromDegrees(180))]),
            "Left Rotation",
        )
        putCommandOnDashboard(
            "Drivetrain",
            DriveToPoses(self.drivetrain,
                         Pose2d(16.08-0.22, 4.77-0.385, Rotation2d.fromDegrees(60)),
                         [Pose2d(15, 4.1, Rotation2d.fromDegrees(30)),
                          Pose2d(14, 4.1, Rotation2d(0))]),
            "Right",
        )

        putCommandOnDashboard(
            "Shooter", ShootAndMovePivotLoading(self.shooter, self.pivot, self.intake)
        )
        putCommandOnDashboard("Shooter", ManualShoot(self.shooter))
        putCommandOnDashboard("Shooter", PrepareShoot(self.shooter, self.pivot))

        putCommandOnDashboard(
            "Vision",
            AlignEverything(
                self.drivetrain, self.pivot, self.vision, self.xbox_controller
            ),
        )

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def teleopInit(self):
        if self.auto_command:
            self.auto_command.cancel()

    def robotPeriodic(self):
        self.vision.periodic()
        super().robotPeriodic()


def putCommandOnDashboard(
    sub_table: str, cmd: commands2.Command, name: str = None, suffix: str = " commands"
) -> commands2.Command:
    if not isinstance(sub_table, str):
        raise ValueError(
            f"sub_table should be a str: '{sub_table}' of type '{type(sub_table)}'"
        )

    if suffix:
        sub_table += suffix

    sub_table += "/"

    if name is None:
        name = cmd.getName()
    else:
        cmd.setName(name)

    wpilib.SmartDashboard.putData(sub_table + name, cmd)

    return cmd
