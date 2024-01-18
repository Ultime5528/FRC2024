from pyfrc.tests import *

import wpilib.simulation
import pytest
from utils.sparkmaxsim import SparkMaxSim
from subsystems.shooter import Shooter


def test_shootHigh(control, robot):

    with control.run_robot():
        robot.shooter.shootHigh()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter.shooter_high_speed == pytest.approx(robot.shooter.left_motor_sim.getVelocity(), rel=0.01)
        assert -1*robot.shooter.shooter_high_speed == pytest.approx(robot.shooter.right_motor_sim.getVelocity(), rel=0.01)


def test_shootLow(control, robot):

    with control.run_robot():
        robot.shooter.shootLow()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        assert robot.shooter.shooter_low_speed == pytest.approx(robot.shooter.left_motor_sim.getVelocity(), rel=0.01)
        assert -1*robot.shooter.shooter_low_speed == pytest.approx(robot.shooter.right_motor_sim.getVelocity(), rel=0.01)




