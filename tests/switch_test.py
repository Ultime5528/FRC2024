import pytest
from utils.switch import Switch


def test_normallyOpened(control):
    with control.run_robot():
        switch = Switch(1, Switch.Type.NormallyOpen)
        # check if NormallyOpen switch is really pressed/unpressed when setSimUnpressed() and setSimPressed are called
        switch.setSimPressed()
        # control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert switch.isPressed()
        assert switch._input.get()
        switch.setSimUnpressed()
        # control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert not switch.isPressed()
        assert not switch._input.get()


def test_normallyClosed(control):
    with control.run_robot():
        switch = Switch(2, Switch.Type.NormallyClosed)
        # check if NormallyClosed switch is really pressed/unpressed when setSimUnpressed() and setSimPressed are called
        switch.setSimPressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert switch.isPressed()
        assert not switch._input.get()
        switch.setSimUnpressed()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert not switch.isPressed()
        assert switch._input.get()


def test_TypeError():
    with pytest.raises(TypeError):
        Switch(1, 3)
