
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import robot_controller as robo


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True


def main():
    ev3.Sound.speak("Snake").wait()
    robot = robo.Snatch3r()
    dc = DataContainer()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    color_sensor = ev3.ColorSensor()

    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)

    while dc.running:

        if int(color_sensor.color) == ev3.ColorSensor.COLOR_RED:
            send_points(mqtt_client)

            time.sleep(1)
            ev3.Sound.speak("10 points").wait()

        if int(color_sensor.color) == ev3.ColorSensor.COLOR_BLACK:
            game_over(mqtt_client)
            time.sleep(1)
            ev3.Sound.speak("Game Over").wait()

        btn.process()
        time.sleep(0.01)

    ev3.Sound.speak("Goodbye").wait()


def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


def send_points(mqtt_client):
    mqtt_client.send_message("sendPoints")


def game_over(mqtt_client):
    mqtt_client.send_message("gameover")


main()
