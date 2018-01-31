"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    
    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)


    def drive_inches(self, inches_target, speed_deg_per_second):
        time_sp = 1  # Any value other than 0.
        while time_sp != 0:
            #speed_deg_per_second = int(input("Enter a speed(0 to 900 dps): "))
            if speed_deg_per_second == 0:
                break

            #inches_target = int(input("Distance to travel (inches): "))
            if speed_deg_per_second == 0:
                break
            self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target * 90, stop_action='brake')
            self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target * 90, stop_action='brake')
            ev3.Sound.beep().wait_while(self.right_motor.STATE_RUNNING)