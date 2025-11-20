import rospy
import math
import socketio
from flask import Flask, request, jsonify

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


class Server:
  action = "stopped" # stopped; started; killed
  
  @app.route("/api/start")
  def apiStart():
    Server.action = "startted"
    return ""
  @app.route("/api/stop")
  def apiStart():
    Server.action = "stopped"
    return ""
  @app.route("/api/kill")
  def apiStart():
    Server.action = "killed"
    return ""
 
  def start():
    app.run(host="0.0.0.0", port="4000")

