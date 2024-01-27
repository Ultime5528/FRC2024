import pytest


def test_extend(control, robot):

    with control.run_robot():
        robot.climber_left.extend()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.climber_speed_up == pytest.approx(
            robot.climber_left.motor_sim.getVelocity(), rel=0.01)


def test_retract(control, robot):

    with control.run_robot():
        robot.climber_left.retract()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.climber_speed_down == pytest.approx(
                    robot.climber_left.motor_sim.getVelocity(), rel=0.01)


def test_stop(control, robot):

    with control.run_robot():
        robot.climber_left.stop()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert 0 == pytest.approx(robot.climber_left.motor_sim.getVelocity())
