import pyfrc.test_support.controller
from hal import AllianceStationID
from wpilib.simulation import DriverStationSim

from robot import Robot


def test_led_modes(
    control: "pyfrc.test_support.controller.TestController", robot: Robot
):
    DriverStationSim.setAllianceStationId(AllianceStationID.kRed1)

    with control.run_robot():
        robot.led.e_stopped()
        robot.led.modeAuto()
        robot.led.modeTeleop()
        robot.led.modeEndgame()
        robot.led.modePickUp()
        robot.led.modeNoteLoaded()
        robot.led.modeShoot()
        robot.led.modeConnected()
        robot.led.modeNotConnected()
        robot.led.rainbow()
