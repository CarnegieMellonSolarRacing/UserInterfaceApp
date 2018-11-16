from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit

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
    updateBatteryLife("100%")
    
if __name__ == '__main__':
    socketio.run(app)