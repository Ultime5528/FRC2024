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
can_min: Final = 1
drivetrain_motor_turning_br: Final = 1
drivetrain_motor_driving_br: Final = 2
drivetrain_motor_turning_bl: Final = 3
drivetrain_motor_driving_bl: Final = 4
drivetrain_motor_driving_fl: Final = 5
drivetrain_motor_turning_fl: Final = 6
drivetrain_motor_turning_fr: Final = 7
drivetrain_motor_driving_fr: Final = 8
climber_motor_right: Final = 9
climber_motor_left: Final = 10
can_max: Final = 10

# PWM


# DIO
dio_min: Final = 0
climber_switch_up_left = 0
climber_switch_up_right = 1
climber_switch_down_left = 2
climber_switch_down_right = 3
dio_max: Final = 3

# PCM

