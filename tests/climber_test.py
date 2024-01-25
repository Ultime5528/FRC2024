import pytest


def test_extendLeft(control, robot):

    with control.run_robot():
        robot.climber.extendLeft()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber.climber_speed_up == pytest.approx(robot.climber.motor_left_sim.getVelocity(), rel=0.01)


def test_extendRight(control, robot):

    with control.run_robot():
        robot.climber.extendRight()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber.climber_speed_up == pytest.approx(robot.climber.motor_right_sim.getVelocity(), rel=0.01)


def test_retractLeft(control, robot):

    with control.run_robot():
        robot.climber.retractLeft()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber.climber_speed_down == pytest.approx(robot.climber.motor_left_sim.getVelocity(), rel=0.01)


def test_retractRight(control, robot):

    with control.run_robot():
        robot.climber.retractRight()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber.climber_speed_down == pytest.approx(robot.climber.motor_right_sim.getVelocity(), rel=0.01)


def test_stopLeft(control, robot):

    with control.run_robot():
        robot.climber.stopLeft()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert 0 == pytest.approx(robot.climber.motor_left_sim.getVelocity())


def test_stopRight(control, robot):

    with control.run_robot():
        robot.climber.stopRight()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert 0 == pytest.approx(robot.climber.motor_right_sim.getVelocity())
