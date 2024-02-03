import pytest
from commands.pivot import resetpivot
from commands.pivot.resetpivot import ResetPivot
from robot import Robot
from utils.switch import Switch


def test_resetCommand(control, robot: Robot):

    with control.run_robot():
        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetPivot(robot.pivot)
        cmd.schedule()

        # Set switch_up and switch_down to "unpressed" and check speed_up
        robot.pivot._switch_up.setSimUnpressed()
        robot.pivot._switch_down.setSimUnpressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.speed_up == pytest.approx(robot.pivot._motor.get(), rel=0.01)

        # Set switch_up to "pressed" and check speed_down
        robot.pivot._switch_up.setSimPressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.speed_down == pytest.approx(robot.pivot._motor.get(), rel=0.01)

        # Set switch_up to "unpressed" and check if motor stops
        robot.pivot._switch_up.setSimUnpressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert 0.0 == pytest.approx(robot.pivot._motor.get(), rel=0.01)

        # Check if encoder has been set to 0 and if command has stopped
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert 0.0 == pytest.approx(robot.pivot._encoder.get(), rel=0.01)
        assert not cmd.isScheduled()
