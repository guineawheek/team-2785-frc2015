from wpilib import *
from math import pi as PI
from sys import stderr
from time import time
from PidDrive import EncoderDrive
class RobotMap:
    """
    The RobotMap is a mapping from the ports sensors and actuators are wired into
    to a variable name. This provides flexibility changing wiring, makes checking
    the wiring easier and significantly reduces the number of magic numbers
    floating around.
    """
    
    # For example to map the left and right motors, you could define the
    # following variables to use with your drivetrain subsystem.
    left_talon = CANTalon(0)
    right_talon = CANTalon(1)
    nostril_talon = CANTalon(2)
    left_talon.enableBrakeMode(True)
    right_talon.enableBrakeMode(True)
    nostril_talon.enableBrakeMode(True)
    
    encoder_ticks = 360
    wheel_d = 8
    dist_for_360 = 37.5 * PI 
    
    right_encoder = Encoder(0,1)
    right_encoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
    right_encoder.setDistancePerPulse(wheel_d/encoder_ticks)
    left_encoder = Encoder(2,3)
    left_encoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
    left_encoder.setDistancePerPulse(wheel_d/RobotMap.encoder_ticks)
    
    chassis = EncoderDrive(left_talon, right_talon, leftEncoder=left_encoder, rightEncoder=right_encoder)
    
    flipper_solenoid = Solenoid(0)
    bakery_solenoid = Solenoid(1)
    
    nostril_switch = DigitalInput(4)
    bakery_switch_r = DigitalInput(5)
    bakery_switch_l = DigitalInput(6)
    compressor = Compressor(0)
    