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
led_strip = 4

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

#PDP
current_swerve_turning_fl = 0
current_swerve_motor_fl = 1
current_pivot_motor = 2
current_grimpeur_gauche = 3
current_grimpeur_droite = 4
current_intake_motor = 5
current_shooter_motor_gauche = 6
current_shooter_motor_droite = 7
current_swerve_motor_bl = 8
current_swerve_turning_bl = 9
current_swerve_turning_br = 10
current_swerve_motor_br = 11
current_swerve_turning_fr = 12
current_swerve_motor_fr = 13