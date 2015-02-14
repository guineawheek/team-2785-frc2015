'''
Created on Feb 14, 2015

@author: LiuDY
'''
from time import time
from PidDrive import EncoderDrive
class command:
    def __init__(self):
        pass
    def start(self):
        pass
    def stop(self):
        pass
    def done(self):
        return True
    def update(self):
        pass
class moveToTote(command):
    def __init__(self, robotclass):
        self.bot = robotclass
    def start(self):
        self.bot.chassis.drive(0.75, 0)
    def stop(self):
        self.bot.chassis.stopMotor()
    def update(self):
        self.bot.chassis.feed()
    def done(self):
        return self.bot.nostril_switch.get()
class moveTote(command):
    kLiftingTime = 10
    def __init__(self, robotclass, up=True):
        self.motor = robotclass.nostril_talon
        self.up = up
        self.__lifting = False
        self.__lifting_timestamp = 0
    def start(self):
        self.__lifting = True
        self.motor.set(1 if self.up else -1)
        self.__lifting_timestamp = time()
    def done(self):
        return time() >= self.__lifting_timestamp + moveTote.kLiftingTime
    def stop(self):
        self.motor.stopMotor()
        self.__lifting = False
    def update(self):
        self.motor.feed()
class move(command):
    def __init__(self, robotclass, dist, power=1, direction=EncoderDrive.kStraight):
        self.bot = robotclass
        self.dist = dist
        self.dir = direction
        self.power = power
    def start(self):
        self.bot.chassis.pidDrive(self.dist, power=self.power, direction=self.dir)
    def done(self):
        return self.bot.chassis.pidDrive.pidDone()
    def stop(self):
        self.bot.chassis.stopPid()
    def update(self):
        self.bot.chassis.feed()
