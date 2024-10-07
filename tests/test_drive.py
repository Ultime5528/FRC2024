import pyfrc.test_support.controller

from commands.drivetrain.resetgyro import ResetGyro
from robot import Robot


def test_ResetGyro(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):

    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetGyro(robot.drivetrain)
        cmd.schedule()
        control.step_timing(seconds=0.5, autonomous=False, enabled=True)
        assert not cmd.isScheduled()
