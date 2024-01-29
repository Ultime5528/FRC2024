import inspect
from pathlib import Path

from commands2 import Subsystem

from utils.safesubsystem import SafeSubsystem


def get_subsystems():
    subsystems = []
    for file in Path("../subsystems").rglob("*.py"):
        module = __import__(str(file).replace("..\\", "").replace("\\", ".").replace(".py", "").replace("/", "."), fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Subsystem) and obj.__name__ != "SafeSubsystem":
                subsystems.append(obj)
    return subsystems

def test_inheritance():
    for obj in get_subsystems():
        assert issubclass(obj, SafeSubsystem), f"{obj.__name__} is not a subclass of SafeSubsystem"