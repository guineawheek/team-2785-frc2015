'''
Created on Jan 30, 2015

@author: LiuDY
'''
from wpilib import *
import math
class EncoderDrive(RobotDrive):
    '''
    classdocs
    '''
    kRight = [-1, 1]
    kLeft = [1, -1]
    kStraight = [1, 1]
    def __init__(self, *args, **kwargs ):
        """
        This class functions exactly like RobotDrive, but with two additional keyword arguments, and
        without support for more than 2 motors (it's not that polished)
        A simple example for a left encoder wired to ports 0 and 1 with the "L" wire on port 0 
        and the "R" wire on port 1, and a right encoder with the "L" on 2 and the "R" on 3 could be:
            encoderdrive = EncoderDrive(0, 1, leftEncoder=Encoder(0,1), rightEncoder=Encoder(2,3)
        :param leftEncoder: an encoder object representing the encoder on the left motor. 
        :param rightEncoder: an encoder object representing the encoder on the right motor
        """
        self.leftEncoder = kwargs.pop("leftEncoder")
        self.rightEncoder = kwargs.pop("rightEncoder")
        super().__init__(*args, **kwargs)
        self.leftEncoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
        self.rightEncoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
        self.leftPid = PIDController(0.5, 0, 0, self.leftEncoder.pidGet, self.__pidwrite_left)
        self.rightPid = PIDController(0.5, 0, 0, self.rightEncoder.pidGet, self.__pidwrite_right)
        self.leftPid.setPercentTolerance(5)
        self.rightPid.setPercentTolerance(5)
    def PidDrive(self, outputMagnitude, curve, distance):
        self.leftPid.disable()
        self.rightPid.disable()
        self.stopMotor()
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        if curve < 0:
            value = math.log(-curve)
            ratio = (value - self.sensitivity) / (value + self.sensitivity)
            if ratio == 0:
                ratio = .0000000001
            leftOutput = outputMagnitude / ratio
            rightOutput = outputMagnitude
        elif curve > 0:
            value = math.log(curve)
            ratio = (value - self.sensitivity) / (value + self.sensitivity)
            if ratio == 0:
                ratio = .0000000001
            leftOutput = outputMagnitude
            rightOutput = outputMagnitude / ratio
        else:
            leftOutput = outputMagnitude
            rightOutput = outputMagnitude
            self.leftPid.setSetpoint(leftOutput*distance)
            self.rightPid.setSetpoint(rightOutput*distance)
            self.leftPid.enable()
            self.rightPid.enable()
        return [leftOutput*distance, rightOutput*distance]
    def pidDrive(self, power, direction, dist):
        self.leftPid.disable()
        self.rightPid.disable()
        self.stopMotor()
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        self.leftPid.setSetpoint(direction*dist)
        self.rightPid.setSetpoint(direction*dist)
    def PidDone(self):
        return self.leftPid.onTarget() and self.rightPid.onTarget()
    def __pidwrite_left(self, v):
        """Wrapper around self.rearLeftMotor.pidwrite to feed MotorSafety. Should not be called directly."""
        self.rearLeftMotor.pidWrite(v)
        self.feed()
    def __pidwrite_right(self, v):
        """Wrapper around self.rearLeftMotor.pidwrite to feed MotorSafety. Should not be called directly."""
        self.rearRightMotor.pidWrite(-v)
        self.feed()