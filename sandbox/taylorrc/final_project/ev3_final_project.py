"""
The Final Project for CSSE120
This is the ev3 code to run on the robot itself
Author: Ryan Taylor
"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com

robot = robo.Snatch3r()

class MyDelegate(object):

    def __init__(self):
        self.running = True

    def set_led(self, led_side_string, led_color_string):

        print("Received: {} {}".format(led_side_string, led_color_string))
        led_side = None
        if led_side_string == "left":
            led_side = ev3.Leds.LEFT
        elif led_side_string == "right":
            led_side = ev3.Leds.RIGHT

        led_color = None
        if led_color_string == "green":
            led_color = ev3.Leds.GREEN
        elif led_color_string == "red":
            led_color = ev3.Leds.RED
        elif led_color_string == "black":
            led_color = ev3.Leds.BLACK

        if led_side is None or led_color is None:
            print("Invalid parameters sent to set_led. led_side_string = {} led_color_string = {}".format(
                led_side_string, led_color_string))
        else:
            ev3.Leds.set_color(led_side, led_color)

    def grab_package(self, item_number):
        """
        Uses the IR sensor's beacon-seeking capabilities to find the package in the "carrier facility".
        The package will only be picked up at this point.

        :param item_number: Allows the IR Sensor to choose which channel to be registered to
        :return: None
        """
        print("is this working")
        if item_number == 'item1':
            channel_number = 1
            ev3.Sound.speak('Grabbing Echo')
            print('Grabbing Echo')
            robot.seek_beacon()
            print('Fire TV found')
            ev3.Sound.speak('Echo found')
            # this would be a great place to add in 'shipping notifications,' callbacks to the mqtt client on the pc

        if item_number == 'item2':
            channel_number = 2
            ev3.Sound.speak('Grabbing Fire TV')
            print('Grabbing Fire TV')
            robot.seek_beacon()
            print('Fire TV found')
            ev3.Sound.speak('Fire TV found')


def main():
    print("--------------------------------------------")
    print(" LED Button communication")
    print(" Press Back to exit when done.")
    print("--------------------------------------------")
    ev3.Sound.speak("LED Button communication").wait()

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    robot.loop_forever()


main()