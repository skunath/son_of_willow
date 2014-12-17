from willow import app, socketio, experiment
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


####
# Admin Views
####
@app.route('/admin')
def admin():
    #experiment.set_users(2)

    print experiment

    return render_template('admin.html')