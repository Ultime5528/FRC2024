import inspect
from pathlib import Path
import ast
from textwrap import dedent
from commands2 import Command, Subsystem

from utils.safecommand import SafeMixin

def transform_path_into_python_import(file):
    return str(file).replace("..\\", "").replace("\\", ".").replace(".py", "")

def get_commands():
    commands = []
    for file in Path("../commands").rglob("*.py"):
        module = __import__(transform_path_into_python_import(file), fromlist=[""])
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Command) and obj.__name__ != "SafeCommand":
                commands.append(obj)
    return commands


def get_arguments(command):
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
