from wpilib.simulation import stepTiming

from commands.pivot.movepivot import MovePivot
from commands.shooter.shoot import Shoot
from commands.shooter.waitshootspeed import WaitShootSpeed
from robot import Robot


def test_ShootFar(control, robot: Robot):
    with control.run_robot():
        robot.pivot._sim_encoder.setDistance(-0.05)
        robot.pivot._has_reset = True
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        cmd_move_pivot = MovePivot.toSpeakerFar(robot.pivot)
        cmd_move_pivot.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        counter = 0

        while not cmd_move_pivot.isScheduled() and counter < 1000:
           stepTiming(0.01)
           counter += 1

        assert counter < 1000, "MovePivot takes too long to finish"

        cmd_shoot = Shoot(robot.shooter, robot.pivot, robot.intake)
        cmd_shoot.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter._left_motor.get() > 0.05


def test_WaitForSpeed(control, robot):
    # For the moment, we only test that the command does not crash.
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        robot.shooter.shoot(500)
        cmd = WaitShootSpeed(robot.shooter)
        cmd.schedule()
        control.step_timing(seconds=5.0, autonomous=False, enabled=True)
        assert cmd.isScheduled()
