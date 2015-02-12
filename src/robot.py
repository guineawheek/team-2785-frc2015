#!/usr/bin/env python3

from wpilib import *
from robot_map import RobotMap
class MyRobot(IterativeRobot):
    
    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.robot = RobotMap
        self.happystick = Joystick(0)
        self.pwr = 1
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.doBindings()
        
    def testPeriodic(self):
        """This function is called periodically during test mode."""
    def doBindings(self):
        self.pwr = (self.happystick.getZ() + 2) / 2
        self.robot.chassis.arcadeDrive(self.pwr * self.happystick.getY(), self.pwr * self.happystick.getX())
        if self.happystick.getRawButton(3):
            self.robot.bakery_solenoid.set(True)
        elif self.happystick.getRawButton(2):
            self.robot.bakery_solenoid.set(False)
        #TODO: add nostril talon SmartDashboard
        if self.happystick.getRawButton(6):
            self.robot.nostril_tal.set(0.25) #
if __name__ == "__main__":
    run(MyRobot)
