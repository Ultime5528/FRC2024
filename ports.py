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
climber_motor_left: Final = 9
climber_motor_right: Final = 10
shooter_motor_left: Final = 11
shooter_motor_right: Final = 12

# PWM
pivot_motor: Final = 0
intake_motor: Final = 1
climber_servo_right: Final = 2
climber_servo_left: Final = 3

# DIO
pivot_switch_down: Final = 0
pivot_switch_up: Final = 1
intake_sensor: Final = 2
climber_left_switch_up = 3
climber_right_switch_up = 4
pivot_encoder_a: Final = 5
pivot_encoder_b: Final = 6
climber_left_switch_down: Final = 8
climber_right_switch_down: Final = 9
