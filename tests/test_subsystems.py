import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import List, Dict

from commands2 import Subsystem

from utils.safesubsystem import SafeSubsystem


def import_submodules(package, recursive=True) -> Dict[str, ModuleType]:
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :type recursive: bool
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


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