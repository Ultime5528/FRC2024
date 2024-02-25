import math
from enum import Enum
from typing import Callable, Union, Tuple, List

import numpy as np
import wpilib
from wpiutil import SendableBuilder

import ports
from utils.property import autoproperty
from utils.safesubsystem import SafeSubsystem


def interpolate(t, color1, color2):
    assert 0 <= t <= 1
    return ((1 - t) * color1 + t * color2).astype(int)


def numpy_interpolation(t: np.ndarray, color1: np.ndarray, color2: np.ndarray):
    assert 0 <= t.min() and t.max() <= 1
    return ((1 - t)[:, np.newaxis] * color1 + t[:, np.newaxis] * color2).astype(int)


Color = Union[np.ndarray, Tuple[int, int, int], List[int]]


class ModeLED(Enum):
    NONE = "none"
    NOTE = "note"


class LEDController(SafeSubsystem):
    # HSV: [Hue(color 0 to 180), Saturation( amount of gray 0 to 255), Value(brightness 0 to 255)
    red_rgb = np.array([255, 0, 0])
    blue_rgb = np.array([0, 0, 255])
    sky_blue_rgb = np.array([0, 205, 255])
    purple_rgb = np.array([108, 0, 250])
    violet_rgb = np.array([205, 0, 255])
    yellow_rgb = np.array([255, 255, 0])
    orange_rgb = np.array([255, 150, 50])
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])
    beige_rgb = np.array([225, 198, 153])
    green_rgb = np.array([0, 255, 0])

    led_number = 190

    speed = autoproperty(0.75)
    white_length = autoproperty(6.0)
    color_period = autoproperty(20.0)
    brightnessValue = autoproperty(10)

    last = 0

    i_values = np.array(led_number)

    def __init__(self):
        super().__init__()
        self.led_strip = wpilib.AddressableLED(ports.led_strip)
        self.buffer = [wpilib.AddressableLED.LEDData() for _ in range(self.led_number)]
        self.led_strip.setLength(len(self.buffer))
        self.time = 0
        self.explosiveness = 0.0
        self.led_strip.start()
        self.mode = ModeLED.NONE

        self.brightness = max(min(100, self.brightnessValue), 0) / 100

    def setRGB(self, i: int, color: Color):
        color = (color * self.brightness).astype(int)
        self.buffer[i].setRGB(*color)

    def dim(self, x):
        return round(x * max(min(1, self.brightnessValue), 0))

    def setAll(self, color_func: Callable[[int], Color]):
        a = np.arange(len(self.buffer))
        for i in np.nditer(a):
            self.setRGB(i, color_func(i))

    def setMode(self, mode: ModeLED):
        self.mode = mode

    def getAllianceColor(self):
        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kBlue:  # blue team
            color = self.blue_rgb
        elif alliance == wpilib.DriverStation.Alliance.kRed:  # red team
            color = self.red_rgb
        else:
            color = self.black
        return color

    def getModeColor(self):
        if self.mode == ModeLED.NOTE:
            return self.orange_rgb
        else:
            return self.getAllianceColor()

    def getModeSecondaryColor(self):
        if self.mode == ModeLED.NOTE:
            return self.getAllianceColor()
        else:
            return self.white

    def e_stopped(self):
        interval = 10
        flash_time = 20
        state = round(self.time / flash_time) % 2

        def getColor(i: int):
            is_color = state - round(i / interval) % 2
            if is_color:
                return self.red_rgb
            else:
                return self.black

        self.setAll(getColor)

    def ModeAuto(self):
        pass

    def ModeTeleop(self):
        pass

    def ModeEndgame(self):
        pixel_value = abs(round(50 * (math.tan(self.time / 30))))
        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            for i in range(self.led_number):
                self.buffer[i].setRGB(pixel_value, 0, 0)
        else:
            for i in range(self.led_number):
                self.buffer[i].setRGB(0, 0, pixel_value)

    def ModeNoteLoaded(self):
        # pixel_value = round((abs(round(255 * math.cos((self.time) / (18 * math.pi))))) * self.brightness)
        # for i in range(self.led_number):
        #     self.buffer[i].setRGB(0, pixel_value, 0)
        pass

    def ModeReadyToShoot(self):
        pass

    def ModeConnected(self):
        pixel_value = round(
            (abs(round(255 * math.cos((self.time) / (18 * math.pi))))) * self.brightness
        )
        for i in range(self.led_number):
            self.buffer[i].setRGB(0, pixel_value, 0)

    def ModeNotConnected(self):
        pixel_value = round(
            abs(127 * self.brightness * (1 + math.cos(self.time / (18 * math.pi))))
        )

        if wpilib.DriverStation.getAlliance() == wpilib.DriverStation.Alliance.kRed:
            for i in range(self.led_number):
                self.buffer[i].setRGB(pixel_value, 0, 0)
        else:
            for i in range(self.led_number):
                self.buffer[i].setRGB(0, 0, pixel_value)

    def periodic(self) -> None:
        start_time = wpilib.getTime()

        self.time += 1
        if wpilib.DriverStation.isEStopped():
            self.e_stopped()
        else:  # the game has started
            if wpilib.DriverStation.isAutonomousEnabled():  # auto
                self.ModeAuto()
            elif wpilib.DriverStation.isTeleopEnabled():  # teleop
                if (
                    wpilib.DriverStation.getMatchTime() == -1.0
                    or wpilib.DriverStation.getMatchTime() > 20
                ):
                    self.ModeTeleop()
                elif wpilib.DriverStation.getMatchTime() > 1:
                    self.ModeEndgame()
            else:  # game hasn't started
                if wpilib.DriverStation.isDSAttached():
                    self.ModeConnected()  # connected to driver station
                else:  # not connected to driver station
                    self.ModeNotConnected()

        self.led_strip.setData(self.buffer)
        wpilib.SmartDashboard.putNumber("led_time", wpilib.getTime() - start_time)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
        builder.addStringProperty("mode", lambda: str(self.mode), lambda _: None)
        builder.addIntegerProperty("time", lambda: self.time, lambda _: None)
