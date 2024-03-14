import ast
import inspect
from textwrap import dedent
from typing import List
from unittest.mock import patch

import pyfrc.test_support.controller
from commands2 import Command, Subsystem, CommandScheduler

from robot import Robot
from tests.utils import import_submodules
from utils.safecommand import SafeMixin, SafeCommand


def get_commands() -> List[Command or None]:
    import commands

    results = import_submodules(commands)
    cmds = []

    for mod in results.values():
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if (
                issubclass(cls, Command)
                and cls.__name__ != "Command"
                and cls.__name__ != "SafeCommand"
                and cls.__name__ != "ConditionalCommand"
                and cls.__name__ != "SequentialCommandGroup"
                and cls.__name__ != "ParallelCommandGroup"
            ):
                cmds.append(cls)
    return cmds


def get_arguments(command: Command):
    return inspect.signature(command.__init__).parameters


def test_inheritance():
    for obj in get_commands():
        assert issubclass(
            obj, SafeMixin
        ), f"{obj.__name__} is not a subclass of SafeCommand"


def test_arguments():
    for obj in get_commands():
        for name, arg in get_arguments(obj).items():
            if name == "self":
                continue
            assert (
                arg.annotation is not arg.empty
            ), f"Argument {name} of {obj.__name__} has no type annotation"


def test_requirements():
    for obj in get_commands():
        if not issubclass(obj, SafeCommand):
            continue
        addReqs = None

        for c in ast.walk(ast.parse(dedent(inspect.getsource(obj.__init__)))):
            if isinstance(c, ast.Call):
                if isinstance(c.func, ast.Attribute):
                    if c.func.attr == "addRequirements":
                        assert (
                            addReqs is None
                        ), f"{obj.__name__} calls addRequirements() multiple times"
                        addReqs = c
                elif isinstance(c.func, ast.Name):
                    if c.func.id == "addRequirements":
                        assert (
                            addReqs is None
                        ), f"{obj.__name__} calls addRequirements() multiple times"
                        addReqs = c
        super_classes = obj.__bases__
        for super_class in super_classes:
            for c in ast.walk(
                ast.parse(dedent(inspect.getsource(super_class.__init__)))
            ):
                if isinstance(c, ast.Call):
                    if isinstance(c.func, ast.Attribute):
                        if c.func.attr == "addRequirements":
                            assert (
                                addReqs is None
                            ), f"{obj.__name__} calls addRequirements() multiple times"
                            addReqs = c
                    elif isinstance(c.func, ast.Name):
                        if c.func.id == "addRequirements":
                            assert (
                                addReqs is None
                            ), f"{obj.__name__} calls addRequirements() multiple times"
                            addReqs = c

        subsystem_args = {}
        for name, arg in get_arguments(obj).items():
            if isinstance(arg.annotation, type) and issubclass(
                arg.annotation, Subsystem
            ):  # if is a class and is subsystem
                subsystem_args[name] = arg

        if addReqs:
            actual_required_subsystems = []
            for arg in addReqs.args:
                if isinstance(arg, ast.Attribute):
                    actual_required_subsystems.append(arg.attr)
                elif isinstance(arg, ast.Name):
                    actual_required_subsystems.append(arg.id)

            for sub_arg in subsystem_args.keys():
                assert (
                    sub_arg in actual_required_subsystems
                ), f"{obj.__name__} does not require {sub_arg}"
        else:
            assert (
                not subsystem_args
            ), f"addRequirements is not called, but should require {subsystem_args}"


def test_command_scheduler_enabled(control: "pyfrc.test_support.controller.TestController", robot: Robot):
    with control.run_robot():
        control.step_timing(seconds=1.0, autonomous=False, enabled=True)
        assert not CommandScheduler.getInstance()._disabled, "CommandScheduler should not be disabled"

        """
        La méthode 'run' du CommandScheduler est passé directement par référence 
        au TimedRobot, donc on ne peut pas la mocker.
        
        On mock plutôt la fonction periodic d'un subsystem, qui doit uniquement
        être appelé par le scheduler.
        """

        with patch.object(robot.drivetrain, "periodic", wraps=robot.drivetrain.periodic) as mock:
            assert mock.call_count == 0
            control.step_timing(seconds=1.0, autonomous=False, enabled=True)
            assert mock.call_count >= 50
