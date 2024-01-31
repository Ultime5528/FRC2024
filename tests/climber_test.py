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
        assert robot.climber_left.speed_up == pytest.approx(robot.climber_left._motor.get())
        robot.climber_left.sim_switch_up.setValue(False)
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert not cmd.isScheduled()
        assert 0.0 == robot.climber_left._motor.get()


def test_retract(control:  "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = RetractClimber(robot.climber_left)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.speed_down == pytest.approx(robot.climber_left._motor.get())
        robot.climber_left.sim_switch_down.setValue(False)
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert not cmd.isScheduled()
        assert 0.0 == robot.climber_right._motor.get()
