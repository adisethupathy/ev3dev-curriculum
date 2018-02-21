
import tkinter
from tkinter import ttk
import math
import mqtt_remote_method_calls as com


class Drawer(object):
    def __init__(self):
        self.sheet = sheet
        self.start_x = 0
        self.start_y = 0
        self.angleslist = []
        self.distanceslist = []


    def set_point(self, x, y):
        self.start_x = x
        self.start_y = y

    def set_line(self, x1, y1):
        self.sheet.create_line(self.start_x, self.start_y, x1, y1)



def main():
    client = com.MqttClient()
    client.connect_to_ev3()

    #creating window

    window = tkinter.Tk()
    window.title = "controller"
    frame = ttk.Frame(window, padding = 10)
    frame.grid()

    controls = "click to make a path for the robot"
    label = ttk.Label(frame, text = controls)
    label.grid()
    sheet = tkinter.Canvas(frame, background = 'white', width = 600, height = 600)
    sheet.grid()
    drawer = Drawer(sheet)

    sheet.bind("<ButtonPress-1>", lambda event: path(event,drawer))

    exit_button = ttk.Button(frame, text ='Exit')
    exit_button.grid()
    exit_button['command'] = lambda: end(client)

    start_button = ttk.Button(frame, text='GO!')
    start_button.grid()
    start_button['command'] = lambda: begin(drawer, client)

    window.mainloop()


def path(event, drawer):
    print('point set at ({}, {})'.format(event.x, event.y))
    color = 'black'

    if drawer.start_x != 0:
        drawer.set_line(color, event.x, event.y)
        angle = math.atan2((event.x - drawer.start_x), (drawer.start_y - event.y))
        degree = math.degrees(angle)

        if math.fabs(degree) > 180:
            if degree < 0:
                degree = 360 - degree
            if degree < 0:
                degree = degree - 360

        distance = math.sqrt((event.x - drawer.start.x) **2 + (event.y - drawer.start_y) ** 2)
        drawer.distanceslist += [distance]
        drawer.angleslist += [degree]

        drawer.set_point(event.x, event.y)


def begin(drawer,client):
    new_angles = [drawer.angle_list[0]]
    for k in range(1, len(drawer.angleslist)):
        new = drawer.angleslist[k] - drawer.angleslist[k - 1]
        new_angles += [new]


    client.send_message('new_run_path', [new_angles, drawer.distanceslist])

def end(client):
    if client:
        client.close()
    exit()

main()





