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
class endcommand(command):
    def done(self):
        return False
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
    kLiftingTime = 2
    def __init__(self, robotclass, up=True):
        self.sol = robotclass.nostril_solenoid
        self.up = up
        self.__lifting_timestamp = 0
    def start(self):
        self.sol.set(self.up)
        self.__lifting_timestamp = time()
    def done(self):
        return time() >= self.__lifting_timestamp + moveTote.kLiftingTime

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
class moveRack(command):
    kLiftingTime = 2
    def __init__(self, robotclass, up=True):
        self.sol = robotclass.bakery_solenoid
        self.up = up
        self.__lifting_timestamp = 0
    def start(self):
        self.sol.set(self.up)
        self.__lifting_timestamp = time()
    def done(self):
        return time() >= self.__lifting_timestamp + moveRack.kLiftingTime