from pytest import approx

from commands.intake.drop import Drop
from commands.intake.pickup import PickUp
from commands.intake.load import Load
from robot import Robot


def test_drop(control, robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        robot.intake._sensor.setSimPressed()
        cmd = Drop(robot.intake)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake.speed_out == approx(robot.intake._motor.get())
        robot.intake._sensor.setSimUnpressed()
        control.step_timing(
            seconds=cmd.drop_delay - 0.2, autonomous=False, enabled=True
        )
        assert robot.intake.speed_out == approx(robot.intake._motor.get())
        control.step_timing(seconds=0.4, autonomous=False, enabled=True)
        assert 0.0 == approx(robot.intake._motor.get())
        assert not cmd.isScheduled()


def test_load(control, robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        robot.intake._sensor.setSimPressed()
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
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        robot.intake._sensor.setSimUnpressed()
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
