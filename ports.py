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
intake_motor: Final = 11

# PWM
pivot_motor: Final = 0
climber_servo_right = 1
climber_servo_left = 2

# DIO
climber_left_switch_up = 0
climber_right_switch_up = 1
climber_left_switch_down = 2
climber_right_switch_down = 3
intake_sensor: Final = 4
pivot_switch_up: Final = 5
pivot_switch_down: Final = 6
pivot_encoder_a: Final = 7
pivot_encoder_b: Final = 8
