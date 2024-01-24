import pytest


def test_ShootHigh(control, robot):

    with control.run_robot():
        robot.shooter.shootHigh()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter.high_speed == pytest.approx(robot.shooter.left_motor_sim.getVelocity(), rel=0.01)
        assert -1*robot.shooter.high_speed == pytest.approx(robot.shooter.right_motor_sim.getVelocity(), rel=0.01)


def test_ShootLow(control, robot):

    with control.run_robot():
        robot.shooter.shootLow()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter.low_speed == pytest.approx(robot.shooter.left_motor_sim.getVelocity(), rel=0.01)
        assert -1*robot.shooter.low_speed == pytest.approx(robot.shooter.right_motor_sim.getVelocity(), rel=0.01)
