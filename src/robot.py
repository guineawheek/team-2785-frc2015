#!/usr/bin/env python3

from wpilib import *
from robot_map import RobotMap
from PidDrive import EncoderDrive
import commands as c
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
        self.currentCommand = c.command()
        self.commands = [
            c.moveToTote(self.robot),
            c.moveTote(self.robot, True),
            c.move(self.robot, -12),
            c.move(self.robot, self.robot.dist_for_360 * 0.25, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.move(self.robot, self.robot.dist_for_360 * 0.125, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.moveTote(self.robot, False),
            c.move(self.robot, -12)
        ]
        SmartDashboard.putBoolean("Reset autonomous commands on next enable? ", True)
        SmartDashboard.putNumber("Speed knob offset?", 0.4)
    def autonomousInit(self):
        self.commands = [
            c.moveToTote(self.robot),
            c.moveTote(self.robot, True),
            c.move(self.robot, -12),
            c.move(self.robot, self.robot.dist_for_360 * 0.25, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.move(self.robot, self.robot.dist_for_360 * 0.125, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.moveTote(self.robot, False),
            c.move(self.robot, -12)
        ] if SmartDashboard.getBoolean("Reset autonomous commands on next enable? ") else self.commands
        self.robot.nostril_solenoid.set(False)
        self.robot.bakery_solenoid.set(False)
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        """
        Strategy:
            move forward 4 feet until recycle limit activated.
            pick up tote.
            move back 1 foot.
            rotate 90 degrees.
            move forward 2 feet
            rotate 45 degrees.
            move forward 2 feet.
            put container down.
            back away 1 foot.
        """
        if self.currentCommand.done():
            self.currentCommand.stop()
            self.currentCommand = self.commands.pop(0)
            self.currentCommand.run()
            return
        else:
            self.currentCommand.update() 
    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.doBindings()
        self.updateData()
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        pass
    def disabledInit(self):
        self.currentCommand.stop()
    def doBindings(self):
        self.pwr = (self.happystick.getZ() + 2) / 2 + SmartDashboard.getNumber("Speed knob offset?")
        self.robot.chassis.arcadeDrive(self.pwr * self.happystick.getY() * self.controlDir, self.pwr * self.happystick.getX() * self.controlDir)
        if self.happystick.getRawButton(3):
            self.robot.bakery_solenoid.set(True)
        elif self.happystick.getRawButton(2):
            self.robot.bakery_solenoid.set(False)
        self.robot.flipper_solenoid.set(self.happystick.getTrigger())

        if self.happystick.getRawButton(5):
            self.robot.nostril_solenoid.set(True)
        elif self.happystick.getRawButton(4):
            self.robot.nostril_solenoid.set(False)

        if self.happystick.getRawButton(6):
            self.robot.left_encoder.reset()
            self.robot.right_encoder.rightEncoder.reset()
        if self.happystick.getRawButton(8):
            self.controlDir = 1
        elif self.happystick.getRawButton(9):
            self.controlDir = -1
    def updateData(self):
        with SmartDashboard as s:
            s.putNumber("Left encoder (in):", self.robot.left_encoder.get())
            s.putNumber("Right encoder (in):", self.robot.right_encoder.get())
            s.putNumber("Joystick speed setting (teleop only):", (self.joystick.getZ() + 2) / 2)
            s.putNumber("Left bakery switch pressed? ", self.robot.bakery_switch_l.get())
            s.putNumber("Right bakery switch pressed? ", self.robot.bakery_switch_r.get())
            s.putNumber("Nostril switch pressed? ", self.robot.nostril_switch.get())
if __name__ == "__main__":
    run(MyRobot)
