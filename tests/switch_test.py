import pytest
from utils.switch import Switch


def test_normallyOpened():
    switch = Switch(1, Switch.Type.NormallyOpen)
    switch.setSimPressed()
    assert switch.isPressed()
    assert switch._input.get()
    switch.setSimUnpressed()
    assert not switch.isPressed()
    assert not switch._input.get()


def test_normallyClosed():
    switch = Switch(1, Switch.Type.NormallyClosed)
    switch.setSimPressed()
    assert switch.isPressed()
    assert not switch._input.get()
    switch.setSimUnpressed()
    assert not switch.isPressed()
    assert switch._input.get()


def test_TypeError():
    with pytest.raises(TypeError):
        Switch(1, 3)
