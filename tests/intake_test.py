import pytest

from commands.intake.drop import Drop
from commands.intake.pickup import PickUp


def test_drop(control, robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = Drop(robot.intake)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.intake.speed_out == pytest.approx(robot.intake.sim_motor.getVelocity(), rel=0.01)


def test_pickUp(control, robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = PickUp(robot.intake)
        cmd.schedule()
        control.step_timing(seconds=(cmd.delay_time-0.1), autonomous=False, enabled=True)
        assert robot.intake.speed_in == pytest.approx(robot.intake.sim_motor.getVelocity(), rel=0.01)
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        assert 0 == robot.intake.sim_motor.getVelocity()
        assert not cmd.isScheduled()

