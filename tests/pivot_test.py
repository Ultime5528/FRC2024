from pytest import approx
from wpilib.simulation import stepTiming

from commands.pivot.movepivot import MovePivot
from commands.pivot.resetpivotdown import ResetPivotDown
from robot import Robot


#def test_resetCommand(control, robot: Robot):
    #with control.run_robot():
        # Enable robot and schedule command
        #control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        #cmd = ResetPivot(robot.pivot)
       # cmd.schedule()
        #control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        # Set switch_up and switch_down to "unpressed" and check speed_up
        #robot.pivot._sim_encoder.setCount(150)  # Set encoder to the middle so no switch is pressed
        #control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        #assert robot.pivot._motor.get() <= 0.001

        # Set switch_up to "pressed" and check speed_down
        #np = robot.pivot._switch_up.isPressed()
        #robot.pivot._sim_encoder.setCount(255)  # Set encoder to the maximum value so switch_up is pressed
        #control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        #c = robot.pivot._sim_encoder.getCount()
        #v = robot.pivot._sim_motor.getSpeed()
       # p = robot.pivot._switch_up.isPressed()
        #assert robot.pivot._motor.get() <= 0.001

        # Set switch_up to "unpressed" and check if motor stops
        #robot.pivot._sim_encoder.setCount(150)  # Set encoder to the middle so no switch is pressed
       # control.step_timing(seconds=3.0, autonomous=False, enabled=True)
       # assert 0.0 == approx(robot.pivot._motor.get(), rel=0.01)

        # Check if encoder has been set to 0 and if command has stopped
       # control.step_timing(seconds=0.1, autonomous=False, enabled=True)
       # assert 0.0 == approx(robot.pivot._encoder.get())
       # assert not cmd.isScheduled()


def test_movePivot_from_swich_down(control, robot: Robot):
    with control.run_robot():

        # Enable robot and schedule command
        robot.pivot._sim_encoder.setDistance(-0.05)  # Set encoder to the minimum value so switch_down is pressed
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
