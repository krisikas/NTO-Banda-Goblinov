import rospy
import math
from flask_socketio import SocketIO 
from flask import Flask, request, jsonify, render_template
import threading
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped 
import json

# Инициализация Flask-приложения и SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class Bringe:
    # Текущее состояние дрона и список труб
    status = "stop"  # возможные значения: "stop", "start", "kill"
    tubes = []

    def __init__(self):
        # Инициализация ROS-ноды и создание паблишера команд
        rospy.init_node('cmd_bridge', anonymous=True)
        self.cmd_pub = rospy.Publisher("/cmd", String, queue_size=10)
        
        # Подписки на топики ROS
        rospy.Subscriber("/tubes", String, self.tubes_callback)
        rospy.Subscriber("/aruco_map/pose", PoseWithCovarianceStamped, self.pos_callback)
        rospy.Subscriber("/status", String, self.drone_status_callback)
        

    def pos_callback(self, msg):
        # Получаем позицию из сообщения и отправляем на фронт через SocketIO
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        socketio.emit('pos', {"x": x, "y": y, "z": z})

    def drone_status_callback(self, msg):
        # Обновляем статус и отправляем его клиентам
        self.status = msg.data
        socketio.emit('status', msg.data)

    def tubes_callback(self, msg):
        # Обновляем список труб и отправляем его клиентам
        self.tubes = json.loads(msg.data)
        socketio.emit('tubes', json.loads(msg.data))

    def send_command(self, command):
        # Публикация текстовой команды в топик /cmd
        msg = String()
        msg.data = command
        self.cmd_pub.publish(msg)

    def spin(self):
        # Основной цикл ROS-ноды
        rospy.spin()


# Создаём глобальный объект моста между ROS и вебом
ros_node = Bringe()


def ros_spin():
    # Функция для запуска ROS-цикла в отдельном потоке
    ros_node.spin()


# Запускаем ROS-цикл в демоническом потоке
ros_thread = threading.Thread(target=ros_spin)
ros_thread.daemon = True
ros_thread.start()


# HTTP-эндпоинт запуска дрона
@app.route("/api/start")
def api_start():
    ros_node.status = "start"
    ros_node.send_command("start")
    return ""


# HTTP-эндпоинт остановки дрона
@app.route("/api/stop")
def api_stop():
    ros_node.status = "stop"
    ros_node.send_command("stop")
    return ""


# HTTP-эндпоинт аварийного завершения killswitch
@app.route("/api/kill")
def api_kill():
    ros_node.status = "kill"
    ros_node.send_command("kill")
    return ""


# Рендер главной страницы с интерфейсом
@app.route("/")
def index():
    return render_template("index.html")


# Обработчик подключения WebSocket-клиента
@socketio.on('connect')
def connect():
    # При подключении отправляем текущий статус и список труб
    socketio.emit("status", ros_node.status)
    socketio.emit('tubes', ros_node.tubes)


def start():
    # Запуск веб-сервера с SocketIO
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        # Корректное завершение ROS-ноды при остановке сервера
        rospy.signal_shutdown("Web server")


if __name__ == "__main__":
    start()
