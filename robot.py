#!/usr/bin/env python3
from typing import Optional

import commands2.button
import wpilib
from commands2.cmd import sequence
from ntcore import NetworkTableInstance
from wpilib import DriverStation, Timer
from wpimath.geometry import Pose2d, Rotation2d

from commands.aligneverything import AlignEverything
from commands.auto.ampsideshoot import AmpSideShoot
from commands.auto.ampsideshootline import AmpSideShootLine
from commands.auto.ampsideshoottwicegofar import (
    AmpSideShootTwiceGoFar,
)
from commands.auto.ampsideshoottwiceline import (
    AmpSideShootTwiceLine,
)
from commands.auto.centershoot import CenterShoot
from commands.auto.centershootline import CenterShootLine
from commands.auto.centershoottwiceline import (
    CenterShootTwiceLine,
)
from commands.auto.megamodeautonome import MegaModeAutonome
from commands.auto.sourcesideshoot import SourceSideShoot
from commands.auto.sourcesideshootgofar import SourceSideShootGoFar
from commands.auto.sourcesideshootline import SourceSideShootLine
from commands.auto.sourcesideshoottwicegofar import (
    SourceSideShootTwiceGoFar,
)
from commands.auto.sourcesideshoottwiceline import (
    SourceSideShootTwiceLine,
)
from commands.climber.extendclimber import ExtendClimber
from commands.climber.forceresetclimber import ForceResetClimber
from commands.climber.lockratchet import LockRatchet
from commands.climber.retractclimber import RetractClimber
from commands.climber.unlockratchet import UnlockRatchet
from commands.drivetoposes import DriveToPoses
from commands.drivetrain.drive import DriveField
from commands.drivetrain.resetgyro import ResetGyro
from commands.drivetrain.resetpose import ResetPose
from commands.intake.drop import Drop
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from commands.intake.alignedpickup import AlignedPickUp
from commands.pivot.forceresetpivot import ForceResetPivot
from commands.pivot.maintainpivot import MaintainPivot
from commands.pivot.movepivot import MovePivot
from commands.pivot.movepivotcontinuous import MovePivotContinuous
from commands.pivot.resetpivotdown import ResetPivotDown
from commands.pivot.resetpivotup import ResetPivotUp
from commands.shooter.manualshoot import ManualShoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import (
    PrepareAndShootAndMovePivotLoading,
    ShootAndMovePivotLoading,
    Shoot,
)
from commands.vibratenote import VibrateNote
from commands.vision.alignwithtag2d import AlignWithTag2D
from subsystems.climber import Climber
from subsystems.climber import climber_left_properties, climber_right_properties
from subsystems.controller import Controller
from subsystems.drivetrain import Drivetrain
from subsystems.intake import Intake
from subsystems.led import LEDController
from subsystems.pivot import Pivot
from subsystems.shooter import Shooter
from subsystems.shootervision import ShooterVision
from subsystems.pickupvision import PickUpVision
from utils.axistrigger import AxisTrigger

loop_delay = 30.0
entry_name_check_time = "/CheckSaveLoop/time"
entry_name_check_mirror = "/CheckSaveLoop/mirror"


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
        self.vision_shooter = ShooterVision()
        self.vision_pick_up = PickUpVision()
        self.led = LEDController(self)
        self.controller = Controller(self.xbox_controller.getHID())

        """
        Default subsystem commands
        """
        self.drivetrain.setDefaultCommand(
            DriveField(self.drivetrain, self.xbox_controller)
        )
        self.pivot.setDefaultCommand(MaintainPivot(self.pivot))
        self.controller.setDefaultCommand(VibrateNote(self.controller, self.intake))

        """
        NetworkTables entries for properties save loop check
        """
        inst = NetworkTableInstance.getDefault()
        self.entry_check_time = inst.getEntry(entry_name_check_time)
        self.entry_check_mirror = inst.getEntry(entry_name_check_mirror)
        self.timer_check = Timer()
        self.timer_check.start()

        """
        Setups
        """
        # self.setupAuto()
        self.setupButtons()
        # self.setupSubsystemOnDashboard()
        self.setupCommandsOnDashboard()

    def setupAuto(self):
        self.auto_chooser.setDefaultOption("Nothing", ResetGyro(self.drivetrain))

        self.auto_chooser.addOption(
            CenterShoot.__name__,
            CenterShoot(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            AmpSideShoot.__name__,
            AmpSideShoot(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            SourceSideShoot.__name__,
            SourceSideShoot(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            CenterShootLine.__name__,
            CenterShootLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            CenterShootTwiceLine.__name__,
            CenterShootTwiceLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
                self.vision_pick_up,
            ),
        )

        self.auto_chooser.addOption(
            AmpSideShootLine.__name__,
            AmpSideShootLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            AmpSideShootTwiceLine.__name__,
            AmpSideShootTwiceLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            SourceSideShootTwiceGoFar.__name__,
            SourceSideShootTwiceGoFar(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            SourceSideShootLine.__name__,
            SourceSideShootLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            SourceSideShootTwiceLine.__name__,
            SourceSideShootTwiceLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            AmpSideShootTwiceGoFar.__name__,
            AmpSideShootTwiceGoFar(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            MegaModeAutonome.__name__,
            MegaModeAutonome(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        self.auto_chooser.addOption(
            SourceSideShootGoFar.__name__,
            SourceSideShootGoFar(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
            ),
        )

        wpilib.SmartDashboard.putData("Autonomous mode", self.auto_chooser)

    def setupButtons(self):
        """
        Bind commands to buttons on controllers and joysticks
        """
        self.xbox_controller.rightTrigger().whileTrue(
            AlignEverything(
                self.drivetrain,
                self.pivot,
                self.shooter,
                self.vision_shooter,
                self.xbox_controller,
            )
        )
        self.xbox_controller.leftTrigger().whileTrue(
            AlignedPickUp(self.drivetrain, self.intake, self.vision_pick_up)
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
        self.panel_2.button(2).onTrue(
            PrepareAndShootAndMovePivotLoading(self.shooter, self.pivot, self.intake)
        )
        self.panel_2.button(5).onTrue(
            ShootAndMovePivotLoading(self.shooter, self.intake, self.pivot)
        )
        self.panel_2.button(1).onTrue(MovePivot.toAmp(self.pivot))
        self.panel_2.button(4).onTrue(ResetPivotDown(self.pivot))

    def setupSubsystemOnDashboard(self):
        wpilib.SmartDashboard.putData("Drivetrain", self.drivetrain)
        wpilib.SmartDashboard.putData("ClimberLeft", self.climber_left)
        wpilib.SmartDashboard.putData("ClimberRight", self.climber_right)
        wpilib.SmartDashboard.putData("Intake", self.intake)
        wpilib.SmartDashboard.putData("Pivot", self.pivot)
        wpilib.SmartDashboard.putData("Shooter", self.shooter)
        wpilib.SmartDashboard.putData("Vision", self.vision_shooter)
        wpilib.SmartDashboard.putData("LED", self.led)
        wpilib.SmartDashboard.putData("Controller", self.controller)

    def setupCommandsOnDashboard(self):
        """
        Send commands to dashboard to
        """
        putCommandOnDashboard(
            "Auto",
            CenterShootTwiceLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
                self.vision_pick_up,
            ),
        )
        CenterShootTwiceLine(
            self.drivetrain,
            self.shooter,
            self.pivot,
            self.intake,
            self.vision_shooter,
            self.vision_pick_up,
        ),

        putCommandOnDashboard(
            "AutoCommand",
            CenterShootTwiceLine(
                self.drivetrain,
                self.shooter,
                self.pivot,
                self.intake,
                self.vision_shooter,
                self.vision_pick_up,
            ),
        )

        putCommandOnDashboard(
            "Drivetrain",
            AlignWithTag2D.toSpeaker(
                self.drivetrain, self.vision_shooter, self.xbox_controller
            ),
        )

        putCommandOnDashboard(
            "Drivetrain",
            sequence(
                ResetPose(
                    self.drivetrain,
                    Pose2d(16.08 - 0.22, 6.33 + 0.385, Rotation2d.fromDegrees(120)),
                ),
                DriveToPoses(
                    self.drivetrain,
                    [
                        Pose2d(15, 7, Rotation2d.fromDegrees(150)),
                        Pose2d(14, 7, Rotation2d.fromDegrees(180)),
                    ],
                ),
            ),
            "Left",
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
        putCommandOnDashboard(
            "Intake", AlignedPickUp(self.drivetrain, self.intake, self.vision_pick_up)
        )

        putCommandOnDashboard("Pivot", MovePivot.toAmp(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerFar(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toSpeakerClose(self.pivot))
        putCommandOnDashboard("Pivot", MovePivot.toLoading(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotDown(self.pivot))
        putCommandOnDashboard("Pivot", ResetPivotUp(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMin(self.pivot))
        putCommandOnDashboard("Pivot", ForceResetPivot.toMax(self.pivot))
        putCommandOnDashboard(
            "Pivot", MovePivotContinuous(self.pivot, self.vision_shooter)
        )

        putCommandOnDashboard(
            "Shooter",
            PrepareAndShootAndMovePivotLoading(self.shooter, self.pivot, self.intake),
        )
        putCommandOnDashboard("Shooter", ManualShoot(self.shooter))
        putCommandOnDashboard("Shooter", PrepareShoot(self.shooter, self.pivot))
        putCommandOnDashboard("Shooter", Shoot(self.shooter, self.intake))

        putCommandOnDashboard(
            "Vision",
            AlignEverything(
                self.drivetrain,
                self.pivot,
                self.shooter,
                self.vision_shooter,
                self.xbox_controller,
            ),
        )

    def autonomousInit(self):
        self.auto_command: commands2.Command = self.auto_chooser.getSelected()
        if self.auto_command:
            self.auto_command.schedule()

    def teleopInit(self):
        if self.auto_command:
            self.auto_command.cancel()
        else:
            ResetGyro(self.drivetrain).schedule()

    def robotPeriodic(self):
        self.checkPropertiesSaveLoop()
        super().robotPeriodic()
        self.vision_shooter.periodic()
        self.vision_pick_up.periodic()

    def checkPropertiesSaveLoop(self):
        from utils.property import mode, PropertyMode

        if mode != PropertyMode.Local:
            if DriverStation.isFMSAttached():
                if self.timer_check.advanceIfElapsed(10.0):
                    wpilib.reportWarning(
                        f"FMS is connected, but PropertyMode is not Local: {mode}"
                    )
            elif DriverStation.isDSAttached():
                self.timer_check.start()
                current_time = wpilib.getTime()
                self.entry_check_time.setDouble(current_time)
                if self.timer_check.advanceIfElapsed(loop_delay):
                    mirror_time = self.entry_check_mirror.getDouble(0.0)
                    if current_time - mirror_time < 5.0:
                        print("Save loop running")
                    else:
                        raise RuntimeError(
                            f"Save loop is not running ({current_time=:.2f}, {mirror_time=:.2f})"
                        )


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
