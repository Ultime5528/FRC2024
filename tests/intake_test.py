import pytest


def test_unload(control, robot):
    with control.run_robot():
        robot.intake.unload()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake.speed_out == pytest.approx(robot.intake.sim_motor.getVelocity(), rel=0.01)