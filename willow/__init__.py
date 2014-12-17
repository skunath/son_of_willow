from gevent import monkey
monkey.patch_all()


from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


from experiment import Experiment

experiment = Experiment()

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
import willow.views
import willow.admin_views