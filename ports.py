from typing import Final

"""
Respect the naming convention : "subsystem" _ "component type" _ "precision"

Put port variables into the right category: CAN - PWM - DIO

Order port numbers, ex:
    drivetrain_motor_fl: Final = 0
    drivetrain_motor_fr: Final = 1
    drivetrain_motor_rr: Final = 2
"""

# CAN
drivetrain_motor_driving_fl: Final = 5
drivetrain_motor_turning_fl: Final = 6
drivetrain_motor_driving_fr: Final = 8
drivetrain_motor_turning_fr: Final = 7
drivetrain_motor_driving_bl: Final = 4
drivetrain_motor_turning_bl: Final = 3
drivetrain_motor_driving_br: Final = 2
drivetrain_motor_turning_br: Final = 1
catapult_motor: Final = 9
intake_motor: Final = 10

# PWM
catapult_servo: Final = 0

# DIO
catapult_limitswitch: Final = 0
intake_sensor: Final = 0

# PCM
catapult_solenoid_forward: Final = 1
catapult_solenoid_reverse: Final = 0
