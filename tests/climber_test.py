import pytest
import pyfrc.test_support.controller

from commands.climber.extendclimber import ExtendClimber
from commands.climber.retractclimber import RetractClimber
from robot import Robot


def test_extend(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ExtendClimber(robot.climber_left)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.speed_up == pytest.approx(
            robot.climber_left._motor.get()
        )
        control.step_timing(seconds=15.0, autonomous=False, enabled=True)
        assert 0.0 == robot.climber_left._motor.get()
        assert robot.climber_left.sim_max_height == pytest.approx(
            robot.climber_left._sim_motor.getPosition(), rel=0.1
        )
        assert not cmd.isScheduled()


def test_retract(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        robot.climber_left._sim_motor.setPosition(robot.climber_left.sim_max_height)
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = RetractClimber(robot.climber_left)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.speed_down == pytest.approx(
            robot.climber_left._motor.get()
        )
        control.step_timing(seconds=15.0, autonomous=False, enabled=True)
        assert not cmd.isScheduled()
        assert robot.climber_left._sim_motor.getPosition() == pytest.approx(
            0.0, rel=0.1
        )
        assert 0.0 == robot.climber_left._motor.get()


def test_requirements(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    with control.run_robot():
        for climber in (robot.climber_right, robot.climber_left):
            cmd = ExtendClimber(climber)
            assert cmd.hasRequirement(climber)
            cmd = RetractClimber(climber)
            assert cmd.hasRequirement(climber)
