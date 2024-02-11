from unittest import mock

import pyfrc.test_support.controller
import rev
from pytest import approx

from commands.intake.drop import Drop
from commands.intake.load import Load
from commands.intake.pickup import PickUp
from robot import Robot


def test_drop(control, robot: Robot):
    with control.run_robot():
        robot.intake._sensor.setSimPressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = Drop(robot.intake)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_out)

        robot.intake._sensor.setSimUnpressed()
        control.step_timing(seconds=cmd.delay - 0.2, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_out)

        control.step_timing(seconds=0.4, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(0.0)
        assert not cmd.isScheduled()


def test_load(control, robot: Robot):
    with control.run_robot():
        robot.intake._sensor.setSimPressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = Load(robot.intake)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_load)

        robot.intake._sensor.setSimUnpressed()
        control.step_timing(seconds=cmd.delay - 0.2, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_load)

        control.step_timing(seconds=0.4, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(0.0)
        assert not cmd.isScheduled()


def test_pickUp(control, robot: Robot):
    with control.run_robot():
        robot.intake._sensor.setSimUnpressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = PickUp(robot.intake)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_in)

        robot.intake._sensor.setSimPressed()
        control.step_timing(seconds=cmd.delay - 0.2, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_in)

        control.step_timing(seconds=0.4, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(0.0)
        assert not cmd.isScheduled()


def test_ports(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        assert robot.intake._motor.getDeviceId() == 11
        assert robot.intake._sensor.getChannel() == 4


@mock.patch("rev.CANSparkMax.restoreFactoryDefaults")
@mock.patch("rev.CANSparkMax.setSmartCurrentLimit")
def test_settings(
        _, __, control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    with control.run_robot():
        assert not robot.intake._motor.getInverted()
        assert robot.intake._motor.getMotorType() == rev.CANSparkMax.MotorType.kBrushless
        assert robot.intake._motor.getIdleMode() == rev.CANSparkMax.IdleMode.kBrake
        robot.intake._motor.restoreFactoryDefaults.assert_called_with()
        robot.intake._motor.setSmartCurrentLimit.assert_called_with(15, 30)


