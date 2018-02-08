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
import traceback
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.MAX_SPEED = 900

        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor

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

    def arm_up(self):
        """Repositions the arm to be in the up state"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")

        ev3.Sound.beep().wait()

    def arm_down(self):
        """Repositions the arm to be in the down state"""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

        ev3.Sound.beep().wait()

    def shutdown(self):
        """Stops all motors and exits the program"""
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

        self.running = False

        print("--------------------------------------------")
        print(" Goodbye")
        print("--------------------------------------------")
        ev3.Sound.speak("Goodbye").wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def forward(self, left_speed, right_speed):
        """Drives the robot forward"""
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def stop(self):
        """Stops both motors"""
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def left(self, left_speed):
        """turns the robot left"""
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=left_speed)

    def right(self, right_speed):
        """Turns the robot right"""
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=right_speed)

    def back(self, left_speed, right_speed):
        """Drives the robot backward"""
        self.right_motor.run_forever(speed_sp=-right_speed)
        self.left_motor.run_forever(speed_sp=-left_speed)

    def seek_beacon(self):
        print("--------------------------------------------")
        print(" Beacon pickup")
        print("--------------------------------------------")
        ev3.Sound.speak("Beacon pickup")

        try:
            while True:
                if seek_beacon(self) is True:
                    print("Found the Beacon")
                    ev3.Sound.speak("Found the Beacon")

                # DONE: 5. Save the result of the seek_beacon function (a bool), then use that value to only say "Found the
                # beacon" if the return value is True.  (i.e. don't say "Found the beacon" if the attempts was cancelled.)


                command = input("Hit enter to seek the beacon again or enter q to quit: ")
                if command == "q":
                    break
        except:
            traceback.print_exc()
            ev3.Sound.speak("Error")

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()


def seek_beacon(robot):
    """
    Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
    If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.

    Type hints:
      :type robot: robo.Snatch3r
      :rtype: bool
    """

    # DONE: 2. Create a BeaconSeeker object on channel 1.
    beacon_seeker = ev3.BeaconSeeker()

    forward_speed = 300
    turn_speed = 100

    while not robot.touch_sensor.is_pressed:
        # The touch sensor can be used to abort the attempt (sometimes handy during testing)

        # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
        current_heading = beacon_seeker.heading  # use the beacon_seeker heading
        current_distance = beacon_seeker.distance  # use the beacon_seeker distance
        if current_distance == -128:
            # If the IR Remote is not found just sit idle for this program until it is moved.
            print("IR Remote not found. Distance is -128")
            robot.stop()
        else:
            # DONE: 4. Implement the following strategy to find the beacon.
            # If the absolute value of the current_heading is less than 2, you are on the right heading.
            #     If the current_distance is 0 return from this function, you have found the beacon!  return True
            #     If the current_distance is greater than 0 drive straight forward (forward_speed, forward_speed)
            # If the absolute value of the current_heading is NOT less than 2 but IS less than 10, you need to spin
            #     If the current_heading is less than 0 turn left (-turn_speed, turn_speed)
            #     If the current_heading is greater than 0 turn right  (turn_speed, -turn_speed)
            # If the absolute value of current_heading is greater than 10, then stop and print Heading too far off
            #
            # Using that plan you should find the beacon if the beacon is in range.  If the beacon is not in range your
            # robot should just sit still until the beacon is placed into view.  It is recommended that you always print
            # something each pass through the loop to help you debug what is going on.  Examples:
            #    print("On the right heading. Distance: ", current_distance)
            #    print("Adjusting heading: ", current_heading)
            #    print("Heading is too far off to fix: ", current_heading)

            # Here is some code to help get you started
            current_heading = beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = beacon_seeker.distance
            if math.fabs(current_heading) < 2:
                # Close enough of a heading to move forward
                print("On the right heading. Distance: ", current_distance)
                # You add more!
                if current_distance == 0:
                    return True
                if current_distance > 0:
                    robot.forward(forward_speed, forward_speed)

            if math.fabs(current_heading) > 2 and math.fabs(current_heading) < 10:
                print("Adjusting Heading: ", current_heading)
                if current_heading < 0:
                    robot.left(turn_speed)
                if current_heading > 0:
                    robot.right(turn_speed)

            if math.fabs(current_heading) > 10:
                robot.stop()
                print("Heading too far off!")

        time.sleep(0.2)

    # The touch_sensor was pressed to abort the attempt if this code runs.
    print("Abandon ship!")
    robot.stop()
    return False