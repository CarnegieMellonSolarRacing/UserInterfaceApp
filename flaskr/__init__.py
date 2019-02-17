from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit
from flask import request
from flask_socketio import join_room, leave_room

import threading
import eventlet
eventlet.monkey_patch()
global path
path = []
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/hello')
def hello():
    return 'Hello, World!'
    
@app.route('/')
def index():
    return render_template('index.html')
    
def updateBatteryLife(value):
    print(value)
    emit('update battery life', value)

@socketio.on('my event')
def handle_message(message):
    print('received message: ' + str(message))
    print('going to send a message now')
    global path
    newPath(path)
    updateBatteryLife("100%")
    

def updatePosition(lat, lon):
    global path
    path.append({"lat":lat, "lng":lon})
    socketio.emit('position', {"lat":lat, "lng":lon})

def clearPath():
    global path
    path = []
    socketio.emit('clear')

def newPath(path):
    socketio.emit('set path', path)

def loop():
    updatePosition(-34.398, 150.650)
    updatePosition(-34.399, 150.651)
    updatePosition(-34.400, 150.66)
    count = 0
    while True:
        count += 1
        print(count)
        updatePosition(-34.4, 150.66 + count/10000)
        eventlet.sleep(.1)

eventlet.spawn(loop)
if __name__ == '__main__':
    socketio.run(app)