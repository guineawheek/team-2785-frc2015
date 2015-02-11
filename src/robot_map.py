from wpilib import *
from math import pi as PI
from sys import stderr
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
    Ltal = CANTalon(0)
    Rtal = CANTalon(1)
    Ltal.enableBrakeMode(True)
    Rtal.enableBrakeMode(True)
    
    right_encoder = Encoder(0,1)
    right_encoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
    left_encoder = Encoder(2,3)
    left_encoder.setPIDSourceParameter(Encoder.PIDSourceParameter.kDistance)
    chassis = EncoderDrive(Jaguar(0), Jaguar(1), leftEncoder=left_encoder, rightEncoder=right_encoder)
    #nostril_window_motor = Jaguar(2)
    nostril_switch = DigitalInput(4)
    nostril_solenoid = Solenoid(0)
    bakery_solenoid = Solenoid(1)
    bakery_switch_r = DigitalInput(5)
    bakery_switch_l = DigitalInput(6)
    compressor = Compressor(0)
    encoder_ticks = 250
    wheel_d = 8/12
    