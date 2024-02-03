import pytest
from pyfrc.tests import *
from wpimath.geometry import Pose2d, Rotation2d
import pyfrc.test_support.controller

from commands.drivetopos import DriveToPos
from robot import Robot


def test_drive_to_poses(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        wanted_pose = Pose2d(1, 2, Rotation2d.fromDegrees(175))
        cmd = DriveToPos(robot.drivetrain, wanted_pose)
        cmd.schedule()
        control.step_timing(seconds=15, autonomous=False, enabled=True)
        assert robot.drivetrain.getPose().X() == pytest.approx(wanted_pose.x, rel=0.01)
        assert robot.drivetrain.getPose().Y() == pytest.approx(wanted_pose.y, rel=0.01)
        assert robot.drivetrain.getAngle() == pytest.approx(wanted_pose.rotation().degrees(), rel=0.01)
