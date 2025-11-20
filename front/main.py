import rospy
import math
from flask_socketio import SocketIO 
from flask import Flask, request, jsonify, render_template
import threading
from std_msgs.msg import String

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class Bringe:
    action = "stopped" # stopped; started; killed
    def __init__(self):
        rospy.init_node('web_bridge', anonymous=True)
        
        self.cmd_pub = rospy.Publisher('/web_action', String, queue_size=10)
        
        rospy.Subscriber('/tubes', String, self.tubes_callback)
        rospy.Subscriber('/telemetry', String, self.telemetry_callback)
        

    def telemetry_callback(self, msg):
        socketio.emit('telemetry', {'data': msg.data})
    def tubes_callback(self, msg):
        socketio.emit('tube', {'data': msg.data})

    def send_command(self, command):
        msg = String()
        msg.data = command
        self.cmd_pub.publish(msg)

    def spin(self):
        rospy.spin()

ros_node = Bringe()

def ros_spin():
    ros_node.spin()

ros_thread = threading.Thread(target=ros_spin)
ros_thread.daemon = True
ros_thread.start()



@app.route("/api/start")
def api_start():
    Bringe.action = "started"
    ros_node.send_command("start")
    return ""
@app.route("/api/stop")
def api_stop():
    Bringe.action = "stopped"
    ros_node.send_command("stop")
    return ""
@app.route("/api/kill")
def api_sill():
    Bringe.action = "killed"
    ros_node.send_command("kill")
    return ""
@app.route("/")
def index():
    return render_template("index.html")

def start():
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

if __name__ == "__main__":
    start()
