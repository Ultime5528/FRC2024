from enum import Enum, auto
from wpilib import DigitalInput, RobotBase
from wpilib.simulation import DIOSim


class Switch:
    class Type(Enum):
        NormallyOpen = auto()  # The switch is False when not pressed
        NormallyClosed = auto()  # The switch is True when not pressed

    def __init__(self, port: int, type: "Switch.Type"):
        self._input = DigitalInput(port)

        if not isinstance(type, Switch.Type):
            raise TypeError(f"Type is not instance of Switch.Type : {type}")

        self._type = type

        if RobotBase.isSimulation:
            self._sim_input = DIOSim(self._input)

            if self._type == Switch.Type.NormallyOpen:
                self._sim_input.setValue(False)
            elif self._type == Switch.Type.NormallyClosed:
                self._sim_input.setValue(True)

    def isPressed(self) -> bool:
        if self._type == Switch.Type.NormallyOpen:
            return self._input.get()
        elif self._type == Switch.Type.NormallyClosed:
            return not self._input.get()
        else:
            raise TypeError(f"Type is not instance of Switch.Type: {type}")

    def setSimPressed(self):
        if not RobotBase.isSimulation():
            raise RuntimeError("setSimPressed should only be called in simulation")
        if self._type == Switch.Type.NormallyOpen:
            self._sim_input.setValue(True)
        elif self._type == Switch.Type.NormallyClosed:
            self._sim_input.setValue(False)

    def setSimUnpressed(self):
        if not RobotBase.isSimulation():
            raise RuntimeError("setSimUnpressed should only be called in simulation")
        if self._type == Switch.Type.NormallyOpen:
            self._sim_input.setValue(False)
        elif self._type == Switch.Type.NormallyClosed:
            self._sim_input.setValue(True)

    def getChannel(self):
        return self._input.getChannel()
