"""
The Final Project for CSSE120
This is the pc code to run on my laptop
Author: Ryan Taylor
"""

import ev3dev.ev3 as ev3
import time

import robot_controller as robo

import tkinter
from tkinter import ttk

from tkinter import *
from PIL import ImageTk, Image

import mqtt_remote_method_calls as com


class MyDelegateOnThePc(object):
    """ Helper class that will receive MQTT messages from the EV3. """

    def __init__(self, label_to_display_messages_in):
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)


def main():
    root = tkinter.Tk()
    root.title("Amazon.com")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_side_item = ttk.Label(main_frame, text="Amazon Echo")
    left_side_item.grid(row=0, column=0)

    photo1 = tkinter.PhotoImage(file='Echo.gif')
    button1 = ttk.Button(main_frame, image=photo1)
    button1.image = photo1
    button1.grid(row=2, column=0)
    # Change this lambda statement
    button1['command'] = lambda: print("Amazon's Echo: The worlds newest voice assistant")

    left_order_button = ttk.Button(main_frame, text="Order Now")
    left_order_button.grid(row=3, column=0)
    left_order_button['command'] = lambda: send_led_command(mqtt_client, "left", "black")

    main_label = ttk.Label(main_frame, text="  Welcome to Amazon  ")
    main_label.grid(row=1, column=1)

    main_space = ttk.Label(main_frame, text="--")
    main_space.grid(row=2, column=1)

    right_side_product = ttk.Label(main_frame, text="Fire TV")
    right_side_product.grid(row=0, column=2)

    photo2 = tkinter.PhotoImage(file='Fire-TV.gif')
    button2 = ttk.Button(main_frame, image=photo2)
    button2.image = photo2
    button2.grid(row=2, column=2)
    # Change this lambda statement
    button2['command'] = lambda: print("Amazon's Fire TV: The newest in streaming")

    right_black_button = ttk.Button(main_frame, text="Order")
    right_black_button.grid(row=3, column=2)
    right_black_button['command'] = lambda: send_led_command(mqtt_client, "right", "black")

    spacer = ttk.Label(main_frame, text="")
    spacer.grid(row=4, column=2)

    address_entry = ttk.Entry(main_frame, width=20)
    address_entry.grid(row=4, column=1)

    address_button = ttk.Button(main_frame, text="Shipping Address:")
    address_button.grid(row=3, column=1)
    address_button['command'] = lambda: address(mqtt_client, address_entry)

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    pc_delegate = MyDelegateOnThePc(spacer)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()
    # mqtt_client.connect_to_ev3("35.194.247.175")  # Off campus IP address of a GCP broker

    root.mainloop()


def send_led_command(mqtt_client, led_side, led_color):
    print("Sending LED side = {}  LED color = {}".format(led_side, led_color))
    mqtt_client.send_message("set_led", [led_side, led_color])


def quit_program(mqtt_client):
    print("Have a nice day!")
    mqtt_client.close()
    exit()


main()
