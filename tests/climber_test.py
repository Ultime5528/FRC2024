from unittest import mock

import pyfrc.test_support.controller
import rev
from pytest import approx
from wpilib.simulation import stepTiming

from commands.climber.extendclimber import ExtendClimber
from commands.climber.forceresetclimber import ForceResetClimber
from commands.climber.lockratchet import LockRatchet
from commands.climber.retractclimber import RetractClimber
from robot import Robot
from subsystems.climber import Climber, climber_left_properties, RatchetState


def test_extend(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        # Put climber at min
        robot.climber_left._sim_motor.setPosition(0.0)
        assert robot.climber_left.ratchet_state == RatchetState.Unknown

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ExtendClimber(robot.climber_left)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        # At the beginning, should unload to unlock ratchet
        assert robot.climber_left._motor.get() == approx(
            robot.climber_left.speed_unload
        )
        assert robot.climber_left._ratchet_servo.get() == approx(
            robot.climber_left.properties.ratchet_unlock_angle
        )
        assert robot.climber_left.ratchet_state == RatchetState.Unknown

        counter = 0

        while (
            robot.climber_left._motor.get() == approx(robot.climber_left.speed_unload)
            and counter < 1000
        ):
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "climber unload takes too long to finish"

        # Leave some for next subcommand to start
        stepTiming(0.1)

        assert robot.climber_left.ratchet_state == RatchetState.Unlocked
        assert robot.climber_left._motor.get() == approx(robot.climber_left.speed_up)

        counter = 0

        while cmd.isScheduled() and counter < 1000:
            stepTiming(0.1)
            counter += 1

        assert counter < 1000, "command takes too long to finish"

        # If simulationPeriodic works, switch stopped climber from going over max
        assert not cmd.isScheduled()
        assert robot.climber_left._motor.get() == approx(0.0)
        assert robot.climber_left._ratchet_servo.get() == approx(
            robot.climber_left.properties.ratchet_unlock_angle
        )


def test_retract(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        # Put climber at half
        robot.climber_left._sim_motor.setPosition(robot.climber_left.sim_max_height / 2)
        assert robot.climber_left.ratchet_state == RatchetState.Unknown

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = RetractClimber(robot.climber_left)
        cmd.schedule()

        # Wait for LockRatchet delay
        stepTiming(LockRatchet(robot.climber_left).delay + 0.1)

        assert robot.climber_left._motor.get() == approx(robot.climber_left.speed_down)
        assert robot.climber_left._ratchet_servo.get() == approx(
            robot.climber_left.properties.ratchet_lock_angle
        )
        assert robot.climber_left.ratchet_state == RatchetState.Locked

        counter = 0

        while cmd.isScheduled() and counter < 1000:
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "command takes too long to finish"

        # If simulationPeriodic works, switch stopped climber from going over max
        assert not cmd.isScheduled()
        assert robot.climber_left._motor.get() == approx(0.0)
        assert robot.climber_left._ratchet_servo.get() == approx(
            robot.climber_left.properties.ratchet_lock_angle
        )


def test_forceresetclimber(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ExtendClimber(robot.climber_left)
        cmd.schedule()
        control.step_timing(seconds=5, autonomous=False, enabled=True)
        cmd = ForceResetClimber.toMax(robot.climber_left)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.climber_left.getHeight() == approx(
            robot.climber_left.properties.height_max
        )


def test_ports(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        # left
        assert robot.climber_left._motor.getDeviceId() == 9
        assert robot.climber_left._switch_up.getChannel() == 3
        assert robot.climber_left._ratchet_servo.getChannel() == 2
        # assert robot.climber_left._switch_down.getChannel() == 2
        # right
        assert robot.climber_right._motor.getDeviceId() == 10
        assert robot.climber_right._switch_up.getChannel() == 4
        assert robot.climber_right._ratchet_servo.getChannel() == 3
        # assert robot.climber_right._switch_down.getChannel() == 3


@mock.patch("rev.CANSparkMax.restoreFactoryDefaults")
@mock.patch("rev.CANSparkMax.setSmartCurrentLimit")
def test_settings(mock_setSmartCurrentLimit, mock_restoreFactoryDefaults):
    mock_restoreFactoryDefaults.assert_not_called()
    mock_setSmartCurrentLimit.assert_not_called()

    climber = Climber(climber_left_properties)

    assert not climber._motor.getInverted()
    assert climber._motor.getMotorType() == rev.CANSparkMax.MotorType.kBrushless
    assert climber._motor.getIdleMode() == rev.CANSparkMax.IdleMode.kBrake
    climber._motor.restoreFactoryDefaults.assert_called_with()


def test_requirements(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    with control.run_robot():
        for climber in (robot.climber_right, robot.climber_left):
            cmd = ExtendClimber(climber)
            assert cmd.hasRequirement(climber)
            cmd = RetractClimber(climber)
            assert cmd.hasRequirement(climber)
