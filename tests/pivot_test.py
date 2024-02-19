import pyfrc.test_support.controller
from pytest import approx
from wpilib.simulation import stepTiming

from commands.pivot.forceresetpivot import ForceResetPivot
from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from robot import Robot


def test_maintain(control, robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot._motor.get() == 0
        robot.pivot.state = robot.pivot.State.Amp
        assert robot.pivot._motor.get() >= robot.pivot.speed_maintain
        robot.pivot.state = robot.pivot.State.Moving
        assert robot.pivot._motor.get() == 0


def test_movePivot_from_swich_down(control, robot: Robot):
    with control.run_robot():

        # Set encoder to the minimum value so switch_down is pressed
        robot.pivot._sim_encoder.setDistance(-0.05)

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.isDown()

        cmd = MovePivot.toSpeakerFar(robot.pivot)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        counter = 0
        while robot.pivot._switch_down.isPressed() and counter < 100:
            assert robot.pivot._motor.get() > 0.0
            stepTiming(0.01)
            counter += 1

        control.step_timing(seconds=5, autonomous=False, enabled=True)
        assert counter < 100, "not isPressed takes too long to happen"
        assert not robot.pivot._switch_down.isPressed()
        assert robot.pivot._motor.get() == approx(0.0)
        assert robot.pivot.getHeight() == approx(155, abs=1.0)


def test_ports(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        # left
        assert robot.pivot._switch_up.getChannel() == 0
        assert robot.pivot._switch_down.getChannel() == 7
        assert robot.pivot._motor.getChannel() == 0


def test_resetCommand(control, robot: Robot):
    with control.run_robot():
        robot.pivot._sim_encoder.setDistance(15.0)

        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetPivotDown(robot.pivot)
        cmd.schedule()

        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        counter = 0
        while not robot.pivot._switch_down.isPressed() and counter < 100:
            assert robot.pivot._motor.get() < 0.0
            s = robot.pivot._motor.get()
            h = robot.pivot.getHeight()
            stepTiming(0.01)
            counter += 1

        assert counter < 100, "isPressed takes too long to happen"
        assert robot.pivot._switch_down.isPressed()

        counter = 0
        while robot.pivot._switch_down.isPressed() and counter < 100:
            assert robot.pivot._motor.get() > 0.0
            s = robot.pivot._motor.get()
            h = robot.pivot.getHeight()
            stepTiming(0.01)
            counter += 1

        assert counter < 100, "not isPressed takes too long to happen"
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
