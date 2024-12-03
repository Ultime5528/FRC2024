from math import floor
from typing import Optional

import math

import wpilib
from commands2 import FunctionalCommand
from numpy.ma.testutils import approx
from pathplannerlib.config import PIDConstants, RobotConfig
from pathplannerlib.controller import PPHolonomicDriveController
from pathplannerlib.path import PathPlannerPath, PathPoint
from pathplannerlib.telemetry import PPLibTelemetry
from pathplannerlib.trajectory import PathPlannerTrajectory
from pathplannerlib.util import DriveFeedforwards
from photonlibpy.photonCamera import PhotonCamera
from wpilib import RobotBase, DriverStation, SmartDashboard
from commands2.command import Command
from wpimath.estimator import SwerveDrive4PoseEstimator
from wpimath.geometry import Pose2d, Translation2d, Rotation2d, Twist2d
from wpimath.kinematics import (
    ChassisSpeeds,
    SwerveDrive4Kinematics,
    SwerveModuleState,
)
from pathplannerlib.auto import AutoBuilder
from wpimath.units import feetToMeters

import ports
from gyro import ADIS16470
from utils.property import autoproperty
from utils.safecommand import SafeCommand
from utils.safesubsystem import SafeSubsystem
from utils.swerve import SwerveModule


def should_flip_path():
    # Boolean supplier that controls when the path will be mirrored for the red alliance
    # This will flip the path being followed to the red side of the field.
    # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
    return DriverStation.getAlliance() == DriverStation.Alliance.kRed


width = 0.597
length = 0.597


class Drivetrain(SafeSubsystem):
    max_angular_speed = autoproperty(25.0)

    angular_offset_fl = autoproperty(-1.57)
    angular_offset_fr = autoproperty(0.0)
    angular_offset_bl = autoproperty(3.14)
    angular_offset_br = autoproperty(1.57)

    should_flip_path = autoproperty(False)

    def __init__(self, period: float) -> None:
        super().__init__()
        self.period_seconds = period

        # Swerve Module motor positions
        self.motor_fl_loc = Translation2d(width / 2, length / 2)
        self.motor_fr_loc = Translation2d(width / 2, -length / 2)
        self.motor_bl_loc = Translation2d(-width / 2, length / 2)
        self.motor_br_loc = Translation2d(-width / 2, -length / 2)

        self.swerve_module_fl = SwerveModule(
            ports.drivetrain_motor_driving_fl,
            ports.drivetrain_motor_turning_fl,
            self.angular_offset_fl,
        )

        self.swerve_module_fr = SwerveModule(
            ports.drivetrain_motor_driving_fr,
            ports.drivetrain_motor_turning_fr,
            self.angular_offset_fr,
        )

        self.swerve_module_bl = SwerveModule(
            ports.drivetrain_motor_driving_bl,
            ports.drivetrain_motor_turning_bl,
            self.angular_offset_bl,
        )

        self.swerve_module_br = SwerveModule(
            ports.drivetrain_motor_driving_br,
            ports.drivetrain_motor_turning_br,
            self.angular_offset_br,
        )

        # Gyro
        """
        Possibilités : NavX, ADIS16448, ADIS16470, ADXRS, Empty
        """
        self._gyro = ADIS16470()
        # TODO Assert _gyro is subclass of abstract class Gyro
        self.addChild("Gyro", self._gyro)

        self._field = wpilib.Field2d()
        wpilib.SmartDashboard.putData("Field", self._field)

        self.swervedrive_kinematics = SwerveDrive4Kinematics(
            self.motor_fl_loc, self.motor_fr_loc, self.motor_bl_loc, self.motor_br_loc
        )

        self.swerve_estimator = SwerveDrive4PoseEstimator(
            self.swervedrive_kinematics,
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            Pose2d(0, 0, 0),
        )

        self.cam = PhotonCamera("mainCamera")

        # AutoBuilder.configureHolonomic(
        #     self.getPose,
        #     self.resetToPose,
        #     self.getRobotRelativeChassisSpeeds,
        #     self.driveFromRobotRelativeChassisSpeeds,
        #     self.swerve_module_fr.getHolonomicPathFollowerConfig(),
        #     should_flip_path,
        #     self,
        # )
        AutoBuilder.configure(
            self.getPose,
            self.resetToPose,
            self.getRobotRelativeChassisSpeeds,
            self.driveFromRobotRelativeChassisSpeeds,
            PPHolonomicDriveController(
                PIDConstants(self.swerve_module_fl.driving_PID_P, 0, 0),
                PIDConstants(self.swerve_module_fl.turning_PID_P, 0, 0),
            ),
            RobotConfig.fromGUISettings(),
            should_flip_path,
            self,
        )
        # AutoBuilder.configureCustom(
        #     self.getCommandFromPathplannerPath,
        #     self.getPose,
        #     self.resetToPose,
        #     should_flip_path,
        # )
        if RobotBase.isSimulation():
            self.sim_yaw = 0

    def drive(
        self,
        x_speed_input: float,
        y_speed_input: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        x_speed = (
            x_speed_input * self.swerve_module_fr.max_speed
        )  # 35 m/s (weird unit, but it works)
        y_speed = y_speed_input * self.swerve_module_fr.max_speed
        rot_speed = rot_speed * self.max_angular_speed
        self.driveRaw(x_speed, y_speed, rot_speed, is_field_relative)

    def driveRaw(
        self,
        x_speed: float,
        y_speed: float,
        rot_speed: float,
        is_field_relative: bool,
    ):
        SmartDashboard.putNumber("driveX", x_speed)
        SmartDashboard.putNumber("driveY", y_speed)
        SmartDashboard.putNumber("driveRot", rot_speed)
        if is_field_relative:
            base_chassis_speed = ChassisSpeeds.fromFieldRelativeSpeeds(
                x_speed, y_speed, rot_speed, self.getPose().rotation()
            )
        else:
            base_chassis_speed = ChassisSpeeds(x_speed, y_speed, rot_speed)

        corrected_chassis_speed = self.correctForDynamics(base_chassis_speed)

        swerve_module_states = self.swervedrive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, self.swerve_module_fr.max_speed
        )
        SmartDashboard.putNumberArray(
            "moduleSpeeds", [state.speed for state in swerve_module_states]
        )

        self.swerve_module_fl.setDesiredState(swerve_module_states[0])
        self.swerve_module_fr.setDesiredState(swerve_module_states[1])
        self.swerve_module_bl.setDesiredState(swerve_module_states[2])
        self.swerve_module_br.setDesiredState(swerve_module_states[3])

    # def getCommandFromPathplannerPath(self, path: PathPlannerPath) -> Command:
    #     return FollowPathplannerPath(
    #         path.flipPath() if should_flip_path() else path, self
    #     )

    def driveFromRobotRelativeChassisSpeeds(
        self, chassis_speeds: ChassisSpeeds, drive_feedforwards: DriveFeedforwards
    ) -> None:
        SmartDashboard.putNumber("chassisSpeedsX", chassis_speeds.vx)
        SmartDashboard.putNumber("chassisSpeedsY", chassis_speeds.vy)
        SmartDashboard.putNumber("chassisSpeedsRot", chassis_speeds.omega_dps)

        corrected_chassis_speed = self.correctForDynamics(chassis_speeds)

        swerve_module_states = self.swervedrive_kinematics.toSwerveModuleStates(
            corrected_chassis_speed
        )

        SwerveDrive4Kinematics.desaturateWheelSpeeds(
            swerve_module_states, self.swerve_module_fr.max_speed
        )
        self.swerve_module_fl.setDesiredState(swerve_module_states[0])
        self.swerve_module_fr.setDesiredState(swerve_module_states[1])
        self.swerve_module_bl.setDesiredState(swerve_module_states[2])
        self.swerve_module_br.setDesiredState(swerve_module_states[3])

    def getAngle(self):
        """
        Wrapped between -180 and 180
        """
        return self._gyro.getAngle()

    def resetGyro(self):
        self._gyro.reset()

    def getPose(self):
        return self.swerve_estimator.getEstimatedPosition()

    def getRobotRelativeChassisSpeeds(self):
        """
        Returns robot relative chassis speeds from current swerve module states
        """
        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        return chassis_speed

    def setXFormation(self):
        """
        Points all the wheels into the center to prevent movement
        """
        self.swerve_module_fl.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )
        self.swerve_module_fr.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_bl.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(-45))
        )
        self.swerve_module_br.setDesiredState(
            SwerveModuleState(0, Rotation2d.fromDegrees(45))
        )

    def stop(self):
        self.swerve_module_fr.stop()
        self.swerve_module_fl.stop()
        self.swerve_module_bl.stop()
        self.swerve_module_br.stop()

    def correctForDynamics(
        self, original_chassis_speeds: ChassisSpeeds
    ) -> ChassisSpeeds:
        next_robot_pose: Pose2d = Pose2d(
            original_chassis_speeds.vx * self.period_seconds,
            original_chassis_speeds.vy * self.period_seconds,
            Rotation2d(original_chassis_speeds.omega * self.period_seconds),
        )
        pose_twist: Twist2d = Pose2d().log(next_robot_pose)
        updated_speeds: ChassisSpeeds = ChassisSpeeds(
            pose_twist.dx / self.period_seconds,
            pose_twist.dy / self.period_seconds,
            pose_twist.dtheta / self.period_seconds,
        )
        return updated_speeds

    def periodic(self):
        self.swerve_estimator.update(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
        )

        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

    def simulationPeriodic(self):
        wpilib.SmartDashboard.putNumberArray(
            "SwerveStates",
            [
                self.swerve_module_fl.getState().angle.radians(),
                self.swerve_module_fl.getState().speed,
                self.swerve_module_fr.getState().angle.radians(),
                self.swerve_module_fr.getState().speed,
                self.swerve_module_bl.getState().angle.radians(),
                self.swerve_module_bl.getState().speed,
                self.swerve_module_br.getState().angle.radians(),
                self.swerve_module_br.getState().speed,
            ],
        )

        self.swerve_module_fl.simulationUpdate(self.period_seconds)
        self.swerve_module_fr.simulationUpdate(self.period_seconds)
        self.swerve_module_bl.simulationUpdate(self.period_seconds)
        self.swerve_module_br.simulationUpdate(self.period_seconds)

        # self.swerve_estimator.update(
        #     self.getPose().rotation(),
        #     (
        #         self.swerve_module_fl.getPosition(),
        #         self.swerve_module_fr.getPosition(),
        #         self.swerve_module_bl.getPosition(),
        #         self.swerve_module_br.getPosition(),
        #     ),
        # )

        module_states = (
            self.swerve_module_fl.getState(),
            self.swerve_module_fr.getState(),
            self.swerve_module_bl.getState(),
            self.swerve_module_br.getState(),
        )
        chassis_speed = self.swervedrive_kinematics.toChassisSpeeds(module_states)
        chassis_rotation_speed = chassis_speed.omega
        self.sim_yaw += chassis_rotation_speed * self.period_seconds
        self._gyro.setSimAngle(math.degrees(self.sim_yaw))

        self._field.setRobotPose(self.swerve_estimator.getEstimatedPosition())

    def resetToPose(self, pose: Optional[Pose2d]):
        self.swerve_estimator.resetPosition(
            self._gyro.getRotation2d(),
            (
                self.swerve_module_fl.getPosition(),
                self.swerve_module_fr.getPosition(),
                self.swerve_module_bl.getPosition(),
                self.swerve_module_br.getPosition(),
            ),
            pose if pose is not None else Pose2d(0, 0, 0),
        )


# class FollowPathplannerPath(SafeCommand):
#     delta_t = autoproperty(0.1)
#     pos_tolerance = autoproperty(0.1)
#     rot_tolerance = autoproperty(1)
#
#     def __init__(self, pathplanner_path: PathPlannerPath, drivetrain: Drivetrain):
#         super().__init__()
#         self.sampled_trajectory = None
#         self.drivetrain = drivetrain
#         self.pathplanner_path = pathplanner_path
#         self.addRequirements(drivetrain)
#         self.sampled_trajectory: list[State] = []
#         self.current_goal = 0
#
#     def initialize(self):
#         self.pathplanner_path = (
#             self.pathplanner_path.flipPath()
#             if should_flip_path()
#             else self.pathplanner_path
#         )
#         PPLibTelemetry.setCurrentPath(self.pathplanner_path)
#         trajectory = self.pathplanner_path.getTrajectory(
#             self.drivetrain.getRobotRelativeChassisSpeeds(),
#             self.drivetrain.getPose().rotation(),
#         )
#
#         for i in range(math.ceil(trajectory.getTotalTimeSeconds() / self.delta_t)):
#             self.sampled_trajectory.append(trajectory.sample(i * self.delta_t))
#
#     def execute(self):
#         PPLibTelemetry.setCurrentPose(self.drivetrain.getPose())
#         PPLibTelemetry.setTargetPose(
#             Pose2d(
#                 self.sampled_trajectory[self.current_goal].positionMeters.X(),
#                 self.sampled_trajectory[self.current_goal].positionMeters.Y(),
#                 self.sampled_trajectory[self.current_goal].positionMeters.angle(),
#             )
#         )
#         position_error = (
#             self.sampled_trajectory[self.current_goal].positionMeters
#             - self.drivetrain.getPose().translation()
#         )
#         rotation_error = (
#             self.sampled_trajectory[self.current_goal].heading
#             - self.drivetrain.getPose().rotation()
#         )
#         if math.hypot(position_error.X(), position_error.Y()) <= self.pos_tolerance:
#             self.current_goal += 1
#         else:
#             self.drivetrain.drive(position_error.X(), position_error.Y(), 0, True)
#
#     def isFinished(self) -> bool:
#         return self.current_goal >= len(self.sampled_trajectory)
#
#     def end(self, interrupted: bool):
#         self.drivetrain.drive(0, 0, 0, True)
