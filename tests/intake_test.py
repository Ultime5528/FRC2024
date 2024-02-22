import pyfrc.test_support.controller
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
        assert robot.intake._motor.get() == approx(robot.intake.speed_out, rel=0.1)

        robot.intake._sensor.setSimUnpressed()
        control.step_timing(seconds=cmd.delay - 0.2, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_out, rel=0.1)

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
        assert robot.intake._motor.get() == approx(robot.intake.speed_load, rel=0.1)

        robot.intake._sensor.setSimUnpressed()
        control.step_timing(seconds=cmd.delay - 0.2, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(robot.intake.speed_load, rel=0.1)

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
        assert robot.intake._motor.get() == approx(robot.intake.speed_in, rel=0.1)

        robot.intake._sensor.setSimPressed()
        control.step_timing(seconds=cmd.delay + 0.1, autonomous=False, enabled=True)
        assert robot.intake._motor.get() == approx(0.0)
        assert not cmd.isScheduled()


def test_ports(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        assert robot.intake._motor.getChannel() == 1
        assert robot.intake._sensor.getChannel() == 2


def test_requirements(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    with control.run_robot():
        cmd = PickUp(robot.intake)
        assert cmd.hasRequirement(robot.intake)
        cmd = Drop(robot.intake)
        assert cmd.hasRequirement(robot.intake)
        cmd = Load(robot.intake)
        assert cmd.hasRequirement(robot.intake)
