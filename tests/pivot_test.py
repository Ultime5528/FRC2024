import pytest


def test_moveUp(control, robot):

    with control.run_robot():
        robot.pivot.moveUp()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.up_speed == pytest.approx(robot.pivot.motor.get(), rel=0.01)


def test_moveDown(control, robot):

    with control.run_robot():
        robot.pivot.moveDown()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.down_speed == pytest.approx(robot.pivot.motor.get(), rel=0.01)


