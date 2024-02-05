import math
from typing import List

from wpimath.controller import PIDController
from wpimath.geometry import Pose2d

from subsystems.drivetrain import Drivetrain
from utils.property import autoproperty
from utils.safecommand import SafeCommand

def distance(p1: Pose2d, p2: Pose2d):
    delta = p1 - p2
    return math.sqrt(delta.x * delta.x + delta.y * delta.y)

def distance2(p1: Pose2d, p2: Pose2d):
    delta = p1 - p2
    return delta.x * delta.x + delta.y * delta.y

def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

class DriveToPoses(SafeCommand):
    pose_p = autoproperty(0.35)
    rot_p = autoproperty(0.0065)

    max_speed = autoproperty(1.0)

    spoof_distance = autoproperty(5.0)

    spoof_radius = autoproperty(1.0)
    spoof_point_radius = autoproperty(0.04)

    last_point_radius = autoproperty(0.04)

    def __init__(self, drivetrain: Drivetrain, waypoints: List[Pose2d]):
        super().__init__()
        self.addRequirements(drivetrain)
        self.drivetrain = drivetrain
        self.waypoints = waypoints
        if len(waypoints) <= 1:
            raise

    def initialize(self):
        self.target_waypoint = 0

        self.pid_x = PIDController(self.pose_p, 0, 0)
        self.pid_y = PIDController(self.pose_p, 0, 0)
        self.pid_rot = PIDController(self.rot_p, 0, 0)
        self.pid_rot.enableContinuousInput(-180, 180)

    def execute(self):
        currRobotPose = self.drivetrain.getPose()
        target = self.waypoints[self.target_waypoint]

        self.pid_x.setSetpoint(target.x)
        self.pid_y.setSetpoint(target.y)
        self.pid_rot.setSetpoint(target.rotation().degrees())
        if self.target_waypoint == len(self.waypoints)-1:
            self.pid_x.setTolerance(self.last_point_radius)
            self.pid_y.setTolerance(self.last_point_radius)
            self.pid_rot.setTolerance(self.last_point_radius)

            if self.pid_x.atSetpoint() and self.pid_y.atSetpoint() and self.pid_rot.atSetpoint(): # is last
                self.target_waypoint += 1
        elif distance2(currRobotPose, target) < self.spoof_point_radius*self.spoof_point_radius:
            self.target_waypoint += 1
        elif distance2(currRobotPose, target) < self.spoof_radius*self.spoof_radius: # is in gaslight radius
            # Calculate Gaslight because under gaslight radius
            deltaX = target.x - currRobotPose.x
            deltaY = target.y - currRobotPose.y

            c = math.sqrt(deltaX*deltaX + deltaY*deltaY) # hypothenuse
            scale_factor = c + self.spoof_distance

            gaslightedX = scale_factor * deltaX + currRobotPose.x
            gaslightedY = scale_factor * deltaY + currRobotPose.y

            self.pid_x.setSetpoint(gaslightedX)
            self.pid_y.setSetpoint(gaslightedY)

        vel_x = self.pid_x.calculate(currRobotPose.x)
        vel_y = self.pid_y.calculate(currRobotPose.y)

        speed = math.sqrt(vel_x * vel_x + vel_y * vel_y)
        clamped_speed = clamp(speed, -self.max_speed, self.max_speed)

        if not math.isclose(speed, 0):
            speed_factor = clamped_speed / speed

            new_vel_x = vel_x * speed_factor
            new_vel_y = vel_y * speed_factor

            self.drivetrain.drive(new_vel_x,
                                  new_vel_y,
                                  -self.pid_rot.calculate(currRobotPose.rotation().degrees()),
                                  True
                                  )

    def isFinished(self) -> bool:
        return self.target_waypoint == len(self.waypoints)

    def end(self, interrupted: bool) -> None:
        self.drivetrain.drive(0, 0, 0, True)