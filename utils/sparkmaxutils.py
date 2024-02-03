from typing import Literal, Optional

import wpilib
from rev import CANSparkMax, REVLibError
from wpilib import RobotBase

IdleMode = Literal["brake", "coast"]

__all__ = ["configureLeader", "configureFollower", "waitForCAN"]


def waitForCAN(time_seconds: float):
    if not RobotBase.isSimulation():
        wpilib.wait(time_seconds)

def configureLeader(motor: CANSparkMax, mode: IdleMode, inverted: bool = False, stallLimit: Optional[int] = None, freeLimit: Optional[int] = None):
    _handleCanError(motor.restoreFactoryDefaults(), "restoreFactoryDefaults", motor)
    motor.setInverted(inverted)
    _configureMotor(motor, mode, stallLimit, freeLimit)


def configureFollower(follower: CANSparkMax, leader: CANSparkMax, mode: IdleMode, inverted: bool = False, stallLimit: Optional[int] = None, freeLimit: Optional[int] = None):
    _handleCanError(follower.restoreFactoryDefaults(), "restoreFactoryDefaults", follower)
    _handleCanError(follower.follow(leader, inverted), "follow", follower)
    _handleCanError(follower.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus0, 1000), "set status0 rate", follower)
    _handleCanError(follower.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus1, 1000), "set status1 rate", follower)
    _handleCanError(follower.setPeriodicFramePeriod(CANSparkMax.PeriodicFrame.kStatus2, 1000), "set status2 rate", follower)
    _configureMotor(follower, mode, stallLimit, freeLimit)


def _configureMotor(motor: CANSparkMax, mode: IdleMode, stallLimit: Optional[int], freeLimit: Optional[int]):
    _handleCanError(motor.setIdleMode(_idleModeToEnum(mode)), "setIdleMode", motor)
    _handleCanError(motor.burnFlash(), "burnFlash", motor)
    _handleCanError(motor.clearFaults(), "clearFaults", motor)

    if stallLimit is not None and freeLimit is not None:
        _handleCanError(motor.setSmartCurrentLimit(stallLimit, freeLimit), "setSmartCurrentLimit", motor)
    elif (stallLimit is None) != (freeLimit is None):
        raise ValueError(f"stallLimit ({stallLimit}) and freeLimit ({freeLimit}) should both have a value.")

    waitForCAN(1.0)


def _idleModeToEnum(mode: IdleMode):
    if mode == "brake":
        return CANSparkMax.IdleMode.kBrake
    elif mode == "coast":
        return CANSparkMax.IdleMode.kCoast
    raise ValueError(f"mode is not 'brake' or 'coast' : {mode}")


def _handleCanError(error: REVLibError, function: str, motor: CANSparkMax):
    if error != REVLibError.kOk:
        wpilib.reportError(f"CANError on motor ID {motor.getDeviceId()} during {function} : {error}", printTrace=True)
