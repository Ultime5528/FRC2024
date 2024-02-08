from utils.safecommand import SafeCommand
from subsystems.shooter import Shooter
from utils.property import autoproperty

class PrepareShoot(SafeCommand):
    speed_far = autoproperty(100)
    close_speed = autoproperty(50)
    amp_speed = autoproperty(25)

    def __init__(self, shooter: Shooter):#, #pivot: Pivot):
        super().__init__()
        self.shooter = shooter
        self.addRequirements(shooter)
        #self.pivot = pivot

    def execute(self):
        #if self.pivot.getPosition == "far":
            #self.shooter.shoot(rpm=self.far_speed)
        #elif self.pivot.getPosition == "close":
            #self.shooter.shoot(rpm=self.close_speed)
        #elif self.pivot.getPosition == "ampl":
            #self.shooter.shoot(rpm=self.ampl_speed)
        #else:
            #raise ValueError(
                #f"Pivot position ({self.pivot.getPosition} is not a existing position."

    def end(self, interrupted: bool):
        self.shooter.stop()
