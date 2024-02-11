from pytest import approx
from commands.pivot import resetdown
from commands.pivot.resetdown import ResetPivot
from robot import Robot
from utils.switch import Switch
from commands.pivot import movepivot
from commands.pivot.movepivot import MovePivot


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
        robot.pivot._sim_encoder.setCount(0)  # Set encoder to the minimum value so switch_down is pressed
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.pivot.isDown()

        cmd = MovePivot.toSpeakerFar(robot.pivot)
        cmd.schedule()

        # Check if motor goes the right way (going up)
        control.step_timing(seconds=5, autonomous=False, enabled=True)
        assert robot.pivot._motor.get() > 0


def test_resetCommand(control, robot: Robot):
    with control.run_robot():
        # Enable robot and schedule command
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        cmd = ResetPivot(robot.pivot)
        cmd.schedule()

        counter = 0
        while not robot.pivot._switch_down.isPressed() and counter < 100:

            assert robot.pivot._motor.get() < 0.0
            control.step_timing(seconds=0.1, autonomous=False, enabled=True)
            counter += 1

        assert counter < 100, "isPressed takes too long tp happen"
        assert robot.pivot._switch_down.isPressed()
        assert 0 == robot.pivot._sim_encoder.getCount()

        counter = 0
        while robot.pivot._switch_down.isPressed() and counter < 100:
            assert robot.pivot._motor.get() > 0.0
            control.step_timing(seconds=0.1, autonomous=False, enabled=True)
            counter += 1

        assert counter < 100, "not isPressed takes too long tp happen"
        assert not robot.pivot._switch_down.isPressed()
        assert 0.0 == approx(robot.pivot._motor.get())

        assert not cmd.isScheduled()