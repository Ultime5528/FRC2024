import inspect
from typing import List
from commands2 import Subsystem

from utils.safesubsystem import SafeSubsystem

from tests.utils import import_submodules


def get_subsystems() -> List[Subsystem or None]:
    import subsystems

    results = import_submodules(subsystems)
    subs = []

    for mod in results.values():
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, Subsystem) and cls.__name__ != "SafeSubsystem":
                subs.append(cls)

    return subs


def test_inheritance():
    for obj in get_subsystems():
        assert issubclass(obj, SafeSubsystem), f"{obj.__name__} is not a subclass of SafeSubsystem"