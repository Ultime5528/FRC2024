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
shooter_motor_left: Final = 11
shooter_motor_right: Final = 12
pivot_motor: Final = 13

# PWM

# DIO
pivot_limitswitch_high: Final = 4
pivot_limitswitch_low: Final = 5
pivot_encoder_a: Final = 6
pivot_encoder_b: Final = 7

# PCM
