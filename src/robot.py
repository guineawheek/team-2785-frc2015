#!/usr/bin/env python3

"""
Strategy:
    move forward 4 feet until recycle limit activated.
    pick up garbage bin.
    move back 1 foot.
    rotate 90 degrees.
    move forward 2 feet
    rotate 45 degrees.
    move forward 2 feet.
    put bin down.
    back away 1 foot.
"""
from wpilib import *
from robot_map import RobotMap
from PidDrive import EncoderDrive

import commands as c
import os

def deepcopy(src):
    ret = []
    for i in range(0, len(src)):
        ret.append(src[i])
    return ret
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
        self.commandTemplate = [
            c.moveToTote(self.robot),
            c.moveTote(self.robot, True),
            c.move(self.robot, -12),
            c.move(self.robot, self.robot.dist_for_360 * 0.25, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.move(self.robot, self.robot.dist_for_360 * 0.125, direction=EncoderDrive.kRight),
            c.move(self.robot, 2*12),
            c.moveTote(self.robot, False),
            c.move(self.robot, -12),
            c.endcommand()
        ]
        self.commands = deepcopy(self.commandTemplate)
        self.autofield = "Reset autonomous commands on next enable? "
        self.speedfield = "Speed knob offset?"
        SmartDashboard.putBoolean(self.autofield, True)
        SmartDashboard.putNumber(self.speedfield, 0.4)
    def autonomousInit(self):
        self.commands = deepcopy(self.commandTemplate) if SmartDashboard.getBoolean(self.autofield) else self.commands
        self.robot.nostril_solenoid.set(False)
        self.robot.bakery_solenoid.set(False)
        self.robot.chassis.setSafetyEnabled(False)
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        
        if self.currentCommand.done():
            self.currentCommand.stop()
            self.currentCommand = self.commands.pop(0)
            self.currentCommand.start()
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
    def doBindings(self):
        self.pwr = (-self.happystick.getZ() + 2) / 2 + SmartDashboard.getNumber(self.speedfield)
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
            self.robot.right_encoder.reset()
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
    try:
        os.system("/usr/bin/env python3 proxy.py & disown")
    except:
        print("No proxy darnit.")
    run(MyRobot)