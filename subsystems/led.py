import math
import weakref
from typing import Callable, Union, Tuple, List

import numpy as np
import wpilib
from wpilib import DriverStation
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


class LEDController(SafeSubsystem):
    # HSV: [Hue(color 0 to 180), Saturation( amount of gray 0 to 255), Value(brightness 0 to 255)
    red_rgb = np.array([255, 0, 0])
    blue_rgb = np.array([0, 0, 255])
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])

    led_number = 190

    brightnessValue = autoproperty(10)

    def __init__(self, robot):
        super().__init__()
        self.led_strip = wpilib.AddressableLED(ports.led_strip)
        self.buffer = [wpilib.AddressableLED.LEDData() for _ in range(self.led_number)]
        self.led_strip.setLength(len(self.buffer))
        self.led_strip.start()

        self.time = 0
        self.timer = wpilib.Timer()

        # Nécessaire pour que les tests puissent bien libérer la mémoire.
        self.robot = weakref.proxy(robot)

    @property
    def brightness(self) -> float:
        return max(min(100, self.brightnessValue), 0) / 100

    def setRGB(self, i: int, color: Color):
        self.buffer[i].setRGB(*color)

    def setAll(self, color_func: Callable[[int], Color]):
        a = np.arange(len(self.buffer))
        for i in np.nditer(a):
            self.setRGB(i, color_func(i))

    def getAllianceColor(self):
        alliance = wpilib.DriverStation.getAlliance()
        if alliance == wpilib.DriverStation.Alliance.kBlue:  # blue team
            color = self.blue_rgb
        elif alliance == wpilib.DriverStation.Alliance.kRed:  # red team
            color = self.red_rgb
        else:
            color = self.black
        return color

    def e_stopped(self):
        interval = 10
        flash_time = 20
        state = round(self.time / flash_time) % 2

        red = (self.brightness * self.red_rgb).astype(int)

        def getColor(i: int):
            is_color = state - round(i / interval) % 2
            if is_color:
                return red
            else:
                return self.black

        self.setAll(getColor)

    def modeAuto(self):
        color = (self.brightness * self.getAllianceColor()).astype(int)
        white = (self.brightness * self.white).astype(int)
        i_values = np.arange(self.led_number)
        y_values = 0.5 * np.sin(2 * math.pi**2 * (i_values - 3 * self.time) / 200) + 0.5

        pixel_value = numpy_interpolation(y_values, color, white)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modeTeleop(self):
        self.commonTeleop(self.getAllianceColor(), self.white, 1.0)

    def modeEndgame(self):
        period = 15
        color = (self.brightness * self.getAllianceColor()).astype(int)
        white = (self.brightness * self.white).astype(int)
        i_values = np.arange(self.led_number)
        y_values = ((i_values - self.time * 1.5) / period) % 1.0

        pixel_value = numpy_interpolation(y_values, color, white)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modePickUp(self):
        self.commonTeleop(self.getAllianceColor(), self.white, 3.0)

    def modeNoteLoaded(self):
        self.commonTeleop(self.white, self.getAllianceColor(), 1.0)

    def commonTeleop(self, color1, color2, speed):
        color1 = (self.brightness * color1).astype(int)
        color2 = (self.brightness * color2).astype(int)

        a = 3
        i_values = np.arange(self.led_number)
        y_values = np.maximum(
            0, (a + 1) * np.cos((i_values - speed * self.time) / 5) - a
        )

        pixel_value = numpy_interpolation(y_values, color1, color2)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modeShoot(self):
        self.timer.start()
        color = (self.brightness * self.getAllianceColor()).astype(int)
        i_values = np.arange(self.led_number)
        y_values = (i_values < (200 * self.timer.get()) % 191).astype(float)

        pixel_value = numpy_interpolation(y_values, self.black, color)
        for i, y in enumerate(pixel_value):
            self.buffer[i].setRGB(*y)

    def modeConnected(self):
        pixel_value = round(
            abs(255 * self.brightness * (math.cos(self.time / (12 * math.pi))))
        )

        if DriverStation.getAlliance() == DriverStation.Alliance.kRed:
            for i in range(self.led_number):
                self.buffer[i].setRGB(pixel_value, 0, 0)
        else:
            for i in range(self.led_number):
                self.buffer[i].setRGB(0, 0, pixel_value)

    def modeNotConnected(self):
        pixel_value = round(
            255 * self.brightness * math.cos(self.time / (18 * math.pi))
        )

        if pixel_value >= 0:
            r = pixel_value
            g = 0
            b = 0
        else:
            r = 0
            g = 0
            b = abs(pixel_value)

        for i in range(self.led_number):
            self.buffer[i].setRGB(r, g, b)

    def rainbow(self):
        for i in range(self.led_number):
            hue = (self.time + int(i * 180 / self.led_number)) % 180
            self.buffer[i].setHSV(
                round(hue * self.brightness),
                round(255 * self.brightness),
                round(255 * self.brightness),
            )

    def periodic(self) -> None:
        from commands.intake.pickup import PickUp

        start_time = wpilib.getTime()
        self.time += 1

        if wpilib.DriverStation.isEStopped():
            self.e_stopped()
        elif wpilib.DriverStation.isAutonomousEnabled():  # auto
            self.modeAuto()
        elif wpilib.DriverStation.isTeleopEnabled():  # teleop
            if wpilib.DriverStation.getMatchTime() > 20:
                if self.robot.shooter.isShooting():
                    self.modeShoot()
                elif self.robot.intake.hasNote():
                    self.modeNoteLoaded()
                elif isinstance(self.robot.intake.getCurrentCommand(), PickUp):
                    self.modePickUp()
                else:
                    self.modeTeleop()
                    self.timer.stop()
                    self.timer.reset()
            elif DriverStation.getMatchTime() == -1.0:
                self.rainbow()
            else:
                self.modeEndgame()
        elif wpilib.DriverStation.isDSAttached():
            self.modeConnected()  # connected to driver station
        else:  # not connected to driver station
            self.modeNotConnected()

        self.led_strip.setData(self.buffer)
        wpilib.SmartDashboard.putNumber("led_time", wpilib.getTime() - start_time)

    def initSendable(self, builder: SendableBuilder) -> None:
        super().initSendable(builder)
        builder.addIntegerProperty("time", lambda: self.time, lambda _: None)
