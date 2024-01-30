import ast
import importlib
import inspect
import pkgutil
import types
from textwrap import dedent
from typing import List, Dict

from commands2 import Command, Subsystem

from utils.safecommand import SafeMixin


def import_submodules(package, recursive=True) -> Dict[str, types.ModuleType]:
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
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


def get_commands() -> List[Command or None]:
    import commands

    results = import_submodules(commands)
    cmds = []

    for mod in results.values():
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, Command) and cls.__name__ != "SafeCommand":
                cmds.append(cls)

    return cmds


def get_arguments(command: Command):
    return inspect.signature(command.__init__).parameters


def test_inheritance():
    for obj in get_commands():
        assert issubclass(obj, SafeMixin), f"{obj.__name__} is not a subclass of SafeCommand"


def test_arguments():
    for obj in get_commands():
        for name, arg in get_arguments(obj).items():
            if name == "self":
                continue
            assert arg.annotation is not arg.empty, f"Argument {name} of {obj.__name__} has no type annotation"


def test_duplicates():
    command_names = [command.__name__ for command in get_commands()]
    for name in command_names:
        assert command_names.count(name) == 1, f"Duplicate command name {name}"


def test_requirements():
    for obj in get_commands():
        addReqs = None

        for c in ast.walk(ast.parse(dedent(inspect.getsource(obj.__init__)))):
            if isinstance(c, ast.Call):
                if isinstance(c.func, ast.Attribute):
                    if c.func.attr == "addRequirements":
                        assert addReqs is None, f"{obj.__name__} calls addRequirements() multiple times"
                        addReqs = c
                elif isinstance(c.func, ast.Name):
                    if c.func.id == "addRequirements":
                        assert addReqs is None, f"{obj.__name__} calls addRequirements() multiple times"
                        addReqs = c
        assert addReqs is not None, f"{obj.__name__} does not call addRequirements()"

        subsystem_args = {}
        for name, arg in get_arguments(obj).items():
            if issubclass(arg.annotation, Subsystem):
                subsystem_args[name] = arg

        actual_required_subsystems = []
        for arg in addReqs.args:
            if isinstance(arg, ast.Attribute):
                actual_required_subsystems.append(arg.attr)
            elif isinstance(arg, ast.Name):
                actual_required_subsystems.append(arg.id)

        for sub_arg in subsystem_args.keys():
            assert sub_arg in actual_required_subsystems, f"{obj.__name__} does not require {sub_arg}"
