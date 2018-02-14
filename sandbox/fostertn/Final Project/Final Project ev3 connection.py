
import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


robot = robo.Snatch3r()
mqtt_client = com.MqttClient(robot)
mqtt_client.connect_to_pc()
robot.loop_forever()  # Avoids letting the robot finish until some "end" command.

    # Pretend like the Snatch3r class has these methods.  The other end can say "shutdown"
def loop_forever(self):
    self.running = True
    while self.running:
            time.sleep(0.1)  # Do nothing until the robot does a shutdown.

def shutdown(self):
    ev3.Sound.speak("Goodbye").wait()
    self.running = False