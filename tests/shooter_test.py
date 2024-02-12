import pytest
from commands.pivot.movepivot import MovePivot
from commands.shooter.shoot import Shoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.waitshootspeed import WaitShootSpeed


def test_ShootFar(control, robot):

    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)


def test_ShootLow(control, robot):

    with control.run_robot():
        robot.shooter.shootLow()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter.low_speed == pytest.approx(
            robot.shooter.left_motor_sim.getVelocity(), rel=0.01
        )
        assert -1 * robot.shooter.low_speed == pytest.approx(
            robot.shooter.right_motor_sim.getVelocity(), rel=0.01
        )
