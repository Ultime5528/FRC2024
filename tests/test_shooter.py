import rev
from pytest import approx
from wpilib.simulation import stepTiming

from commands.pivot.movepivot import MovePivot
from commands.shooter.manualshoot import ManualShoot
from commands.shooter.prepareshoot import PrepareShoot
from commands.shooter.shoot import PrepareAndShootAndMovePivotLoading
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

        while cmd_move_pivot.isScheduled() and counter < 1000:
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "MovePivot takes too long to finish"
        assert not cmd_move_pivot.isScheduled()

        assert not robot.shooter._reached_speed_left
        assert not robot.shooter._reached_speed_right

        prepare_shoot_properties = PrepareShoot(robot.shooter, robot.pivot)
        cmd_shoot = PrepareAndShootAndMovePivotLoading(
            robot.shooter, robot.pivot, robot.intake
        )
        cmd_shoot.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        assert robot.shooter._reached_speed_left
        assert robot.shooter._reached_speed_right
        assert robot.shooter._ref_rpm == approx(prepare_shoot_properties.speed_max)


def test_WaitForSpeed(control, robot):
    # For the moment, we only test that the command does not crash.
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = WaitShootSpeed(robot.shooter)
        cmd.schedule()

        counter = 0

        while cmd.isScheduled() and counter < 200:
            robot.shooter.shoot(1500)
            stepTiming(0.05)
            counter += 1

        assert counter < 200, "Command takes too long to finish"
        assert not cmd.isScheduled()


def test_ports(control, robot):
    with control.run_robot():
        assert robot.shooter._left_motor.getDeviceId() == 11
        assert robot.shooter._right_motor.getDeviceId() == 12


def test_settings(control, robot):
    with control.run_robot():
        # left
        assert not robot.shooter._left_motor.getInverted()
        assert (
            robot.shooter._left_motor.getMotorType()
            == rev.CANSparkMax.MotorType.kBrushless
        )
        assert (
            robot.shooter._left_motor.getIdleMode() == rev.CANSparkMax.IdleMode.kCoast
        )
        # right
        assert robot.shooter._right_motor.getInverted()
        assert (
            robot.shooter._right_motor.getMotorType()
            == rev.CANSparkMax.MotorType.kBrushless
        )
        assert (
            robot.shooter._right_motor.getIdleMode() == rev.CANSparkMax.IdleMode.kCoast
        )


def test_requirements(control, robot):
    with control.run_robot():
        cmd = PrepareShoot(robot.shooter, robot.pivot)
        assert cmd.hasRequirement(robot.shooter)
        cmd = ManualShoot(robot.shooter)
        assert cmd.hasRequirement(robot.shooter)
        cmd = WaitShootSpeed(robot.shooter)
        assert not cmd.hasRequirement(robot.shooter)
