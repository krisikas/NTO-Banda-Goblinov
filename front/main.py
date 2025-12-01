import rospy
import math
from flask_socketio import SocketIO 
from flask import Flask, request, jsonify, render_template
import threading
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped 
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class Bringe:
    status = "stop" # stop; start; kill
    tubes = []
    def __init__(self):
        rospy.init_node('cmd_bridge', anonymous=True)
        self.cmd_pub = rospy.Publisher("/cmd", String, queue_size=10)
        
        rospy.Subscriber("/tubes", String, self.tubes_callback)
        rospy.Subscriber("/aruco_map/pose", PoseWithCovarianceStamped, self.pos_callback)
        rospy.Subscriber("/status", String, self.drone_status_callback)
        

    def pos_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        socketio.emit('pos', {"x": x, "y": y, "z": z})

    def drone_status_callback(self, msg):
        self.status = msg.data
        socketio.emit('status', msg.data)

    def tubes_callback(self, msg):
        self.tubes = json.loads(msg.data)
        socketio.emit('tubes', json.loads(msg.data))

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
    ros_node.status = "start"
    ros_node.send_command("start")
    return ""
@app.route("/api/stop")
def api_stop():
    ros_node.status = "stop"
    ros_node.send_command("stop")
    return ""
@app.route("/api/kill")
def api_kill():
    ros_node.status = "kill"
    ros_node.send_command("kill")
    return ""
@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('connect')
def connect():
    socketio.emit("status", ros_node.status)
    socketio.emit('tubes', ros_node.tubes)


def start():
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        rospy.signal_shutdown("Web server")

if __name__ == "__main__":
    start()
