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
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Allows the robot to drive to a target distance at a given speed"""
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target * 90,
                                       stop_action='brake')
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target * 90,
                                        stop_action='brake')

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Causes the robot to turn a set number of degrees."""

        # Left Turn
        if degrees_to_turn > 0:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.5)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*-4.5)

        # Right Turn
        if degrees_to_turn < 0:
            self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.5)
            self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*-4.5)

        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive_polygon(self, number_of_sides, speed, edge_length_in):
        """Makes a polygon with the given number of sides at the given speed"""

        for k in range(number_of_sides):
            self.drive_inches(edge_length_in, speed)
            self.turn_degrees(360/number_of_sides, speed)

    def arm_calibration(self, state):
        """Resets the position of the arm to be in the down position"""
        if state:
            self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
            while not self.touch_sensor.is_pressed:
                time.sleep(1.00)
            self.arm_motor.stop(stop_action="brake")
            ev3.Sound.beep().wait()

            arm_revolutions_for_full_range = 14.2 * 360
            self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
            self.arm_motor.wait_while(self.arm_motor.STATE_RUNNING)

            self.arm_motor.position = 0

    def arm_up(self, state):
        """Repositions the arm to be in the up state"""
        if state:
            self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
            while not self.touch_sensor.is_pressed:
                time.sleep(0.01)
            self.arm_motor.stop(stop_action="brake")

            ev3.Sound.beep().wait()

    def arm_down(self, state):
        """Repositions the arm to be in the down state"""
        if state:
            self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
            self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

            ev3.Sound.beep().wait()

    def shutdown(self):
        """Stops all motors and exits the program"""
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

        print("--------------------------------------------")
        print(" Goodbye")
        print("--------------------------------------------")
        ev3.Sound.speak("Goodbye").wait()