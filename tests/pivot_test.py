from unittest import mock

import pyfrc.test_support.controller
import wpilib
from pytest import approx
from wpilib.simulation import stepTiming

from commands.pivot.forceresetpivot import ForceResetPivot
from commands.pivot.movepivot import MovePivot
from commands.pivot.movepivot import move_pivot_properties
from commands.pivot.resetpivotdown import ResetPivotDown
from robot import Robot
from subsystems.pivot import Pivot
from utils.switch import Switch


def test_maintain(control, robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot._motor.get() == 0
        robot.pivot.state = robot.pivot.State.Amp
        assert robot.pivot._motor.get() >= robot.pivot.speed_maintain
        robot.pivot.state = robot.pivot.State.Moving
        assert robot.pivot._motor.get() == 0


def common_test_movePivot_from_switch_down(
    control, robot: Robot, MovePivotMethod, wantedHeight
):
    with control.run_robot():
        # Set hasReset to true
        robot.pivot._has_reset = True
        # Set encoder to the minimum value so switch_down is pressed
        robot.pivot._sim_encoder.setDistance(-0.05)
        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.isDown()

        cmd = MovePivotMethod(robot.pivot)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        counter = 0
        assert robot.pivot._motor.get() > 0.0
        while robot.pivot._switch_down.isPressed() and counter < 1000:
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "not isPressed takes too long to happen"
        assert not robot.pivot._switch_down.isPressed()

        while robot.pivot._motor.get() > 0.0 and counter < 1000:
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "the motor takes too long to stop"
        assert robot.pivot._motor.get() == approx(0.0)
        assert robot.pivot.getHeight() == approx(wantedHeight, rel=0.1)


def test_movePivot_toSpeakerFar(control, robot: Robot):
    common_test_movePivot_from_switch_down(
        control,
        robot,
        MovePivot.toSpeakerFar,
        move_pivot_properties.position_speaker_far,
    )


def test_movePivot_toSpeakerClose(control, robot: Robot):
    common_test_movePivot_from_switch_down(
        control,
        robot,
        MovePivot.toSpeakerClose,
        move_pivot_properties.position_speaker_close,
    )


def test_movePivot_toAmp(control, robot: Robot):
    common_test_movePivot_from_switch_down(
        control, robot, MovePivot.toAmp, move_pivot_properties.position_amp
    )


def test_movePivot_toLoading(control, robot: Robot):
    common_test_movePivot_from_switch_down(
        control, robot, MovePivot.toLoading, move_pivot_properties.position_loading
    )


def test_resetCommand(control, robot: Robot):
    with control.run_robot():
        robot.pivot._sim_encoder.setDistance(30.0)

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetPivotDown(robot.pivot)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        counter = 0
        while not robot.pivot._switch_down.isPressed() and counter < 1000:
            assert robot.pivot._motor.get() < 0.0
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "isPressed takes too long to happen"
        assert robot.pivot._switch_down.isPressed()

        counter = 0
        while robot.pivot._switch_down.isPressed() and counter < 1000:
            assert robot.pivot._motor.get() > 0.0
            stepTiming(0.01)
            counter += 1

        assert counter < 1000, "not isPressed takes too long to happen"
        assert not robot.pivot._switch_down.isPressed()
        assert robot.pivot._motor.get() == approx(0.0)
        assert robot.pivot.getHeight() == approx(0.0, abs=1.0)

        assert not cmd.isScheduled()


def test_forceResetPivot(control, robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ForceResetPivot.toMax(robot.pivot)
        cmd.schedule()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.height_max == approx(robot.pivot.getHeight())


def common_test_requirements(
    control: "pyfrc.test_support.controller.TestController",
    robot: Robot,
    MovePivotMethod,
):
    with control.run_robot():
        cmd = MovePivotMethod(robot.pivot)
        assert cmd.hasRequirement(robot.pivot)


def test_requirements_toSpeakerFar(control, robot: Robot):
    common_test_requirements(control, robot, MovePivot.toSpeakerFar)


def test_requirements_toSpeakerClose(control, robot: Robot):
    common_test_requirements(control, robot, MovePivot.toSpeakerClose)


def test_requirements_toAmp(control, robot: Robot):
    common_test_requirements(control, robot, MovePivot.toAmp)


def test_requirements_toLoading(control, robot: Robot):
    common_test_requirements(control, robot, MovePivot.toLoading)


def test_requirements_ResetPivotDown(control, robot: Robot):
    common_test_requirements(control, robot, ResetPivotDown)


@mock.patch("wpilib.Encoder", wraps=wpilib.Encoder)
def test_ports(mock_Encoder):
    mock_Encoder.assert_not_called()

    pivot = Pivot()

    assert pivot._motor.getChannel() == 0
    mock_Encoder.assert_called_once_with(5, 6, reverseDirection=True)
    assert pivot._switch_down.getChannel() == 0
    assert pivot._switch_up.getChannel() == 1


def test_settings():
    pivot = Pivot()

    assert not pivot._motor.getInverted()
    assert pivot._switch_up.getType() == Switch.Type.NormallyClosed
    assert pivot._switch_up.getType() == Switch.Type.NormallyClosed
