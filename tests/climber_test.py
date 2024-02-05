from unittest import mock

import pyfrc.test_support.controller
import pytest
import rev

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


def test_ports(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        # left
        assert robot.climber_left._motor.getDeviceId() == 10
        assert robot.climber_left._switch_up.getChannel() == 0
        assert robot.climber_left._switch_down.getChannel() == 2
        # right
        assert robot.climber_right._motor.getDeviceId() == 9
        assert robot.climber_right._switch_up.getChannel() == 1
        assert robot.climber_right._switch_down.getChannel() == 3


@mock.patch("rev.CANSparkMax.restoreFactoryDefaults")
@mock.patch("rev.CANSparkMax.setSmartCurrentLimit")
def test_settings(_, __, control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        for climber in (robot.climber_left, robot.climber_right):
            assert not climber._motor.getInverted()
            assert climber._motor.getMotorType() == rev.CANSparkMax.MotorType.kBrushless
            assert climber._motor.getIdleMode() == rev.CANSparkMax.IdleMode.kBrake
            climber._motor.restoreFactoryDefaults.assert_called_with()
            climber._motor.setSmartCurrentLimit.assert_called_with(15, 30)
