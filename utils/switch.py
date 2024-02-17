from enum import Enum, auto
from typing import Optional

from wpilib import DigitalInput, RobotBase
from wpilib.simulation import DIOSim


class Switch:
    class Type(Enum):
        NormallyOpen = auto()  # The switch is False when not pressed
        NormallyClosed = auto()  # The switch is True when not pressed
        AlwaysPressed = auto()  # The switch is always open
        AlwaysUnPressed = auto()  # The switch is always close

    def __init__(self, type: "Switch.Type", port: Optional[int] = None):

        if type == Switch.Type.NormallyClosed or type == Switch.Type.NormallyOpen:
            self._input = DigitalInput(port)

        if not isinstance(type, Switch.Type):
            raise TypeError(f"Type is not instance of Switch.Type : {type}")

        self._type = type

        if RobotBase.isSimulation:

            if self._type == Switch.Type.NormallyOpen:
                self._sim_input = DIOSim(self._input)
                self._sim_input.setValue(False)
            elif self._type == Switch.Type.NormallyClosed:
                self._sim_input = DIOSim(self._input)
                self._sim_input.setValue(True)
            elif self._type == Switch.Type.AlwaysPressed:
                self._sim_switch_state = True
            elif self._type == Switch.Type.AlwaysUnPressed:
                self._sim_switch_state = False

    def isPressed(self) -> bool:
        if self._type == Switch.Type.NormallyOpen:
            return self._input.get()
        elif self._type == Switch.Type.NormallyClosed:
            return not self._input.get()
        elif self._type == Switch.Type.AlwaysPressed:
            return self._sim_switch_state
        elif self._type == Switch.Type.AlwaysUnPressed:
            return self._sim_switch_state
        else:
            raise TypeError(f"Type is not instance of Switch.Type: {type}")

    def setSimPressed(self):
        if not RobotBase.isSimulation():
            raise RuntimeError("setSimPressed should only be called in simulation")
        if self._type == Switch.Type.NormallyOpen:
            self._sim_input.setValue(True)
        elif self._type == Switch.Type.NormallyClosed:
            self._sim_input.setValue(False)
        elif self._type == Switch.Type.AlwaysPressed:
            self._sim_switch_state = True
        elif self._type == Switch.Type.AlwaysUnPressed:
            self._sim_switch_state = True

    def setSimUnpressed(self):
        if not RobotBase.isSimulation():
            raise RuntimeError("setSimUnpressed should only be called in simulation")
        if self._type == Switch.Type.NormallyOpen:
            self._sim_input.setValue(False)
        elif self._type == Switch.Type.NormallyClosed:
            self._sim_input.setValue(True)
        elif self._type == Switch.Type.AlwaysPressed:
            self._sim_switch_state = False
        elif self._type == Switch.Type.AlwaysUnPressed:
            self._sim_switch_state = False

    def getChannel(self):
        return self._input.getChannel()
