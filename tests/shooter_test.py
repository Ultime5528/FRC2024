import pytest
from commands.pivot.movepivot import MovePivot
from wpilib.simulation import stepTiming
from commands.shooter.shoot import Shoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from pytest import approx


def test_ShootFar(control, robot):

    with control.run_robot():
        robot.pivot._sim_encoder.setDistance(-0.05)
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = MovePivot.toSpeakerFar(robot.pivot)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        counter = 0
        while robot.pivot._switch_down.isPressed() and counter < 100:
            stepTiming(0.01)
            counter += 1
        control.step_timing(seconds=5, autonomous=False, enabled=True)
        cmd = Shoot(robot.shooter, robot.pivot, robot.intake)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert PrepareShoot.speed_far == approx(robot.shooter._left_motor.get())
