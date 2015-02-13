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
        self.controlDir = 1
        SmartDashboard.putNumber("Nostril talon speed, put values 0 to 1: ", 1)
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        pass

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.doBindings()
        self.updateData()
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass
    def doBindings(self):
        self.pwr = (self.happystick.getZ() + 2) / 2
        self.robot.chassis.arcadeDrive(self.pwr * self.happystick.getY() * self.controlDir, self.pwr * self.happystick.getX() * self.controlDir)
        if self.happystick.getRawButton(3):
            self.robot.bakery_solenoid.set(True)
        elif self.happystick.getRawButton(2):
            self.robot.bakery_solenoid.set(False)
        self.robot.flipper_solenoid.set(self.happystick.getTrigger())

        if self.happystick.getRawButton(5):
            self.robot.nostril_talon.set(SmartDashboard.getNumber("Nostril talon speed, put values 0 to 1: "))
        elif self.happystick.getRawButton(4):
            self.robot.nostril_talon.set(-SmartDashboard.getNumber("Nostril talon speed, put values 0 to 1: "))
        else:
            self.robot.nostril_tal.stopMotor()
        if self.happystick.getRawButton(6):
            self.robot.left_encoder.reset()
            self.robot.right_encoder.rightEncoder.reset()
        if self.happystick.getRawButton(11):
            self.controlDir = 1
        elif self.happystick.getRawButton(10):
            self.controlDir = -1
    def updateData(self):
        with SmartDashboard as s:
            s.putNumber("Left encoder (feet):", self.robot.left_encoder.get())
            s.putNumber("Right encoder (feet):", self.robot.right_encoder.get())
            s.putNumber("Joystick speed setting (teleop only):", (self.joystick.getZ() + 2) / 2)
            s.putNumber("Left bakery switch pressed? ", self.robot.bakery_switch_l.get())
            s.putNumber("Right bakery switch pressed? ", self.robot.bakery_switch_r.get())
            s.putNumber("Nostril switch pressed? ", self.robot.nostril_switch.get())
if __name__ == "__main__":
    run(MyRobot)
