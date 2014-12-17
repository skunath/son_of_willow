from willow import app, socketio, experiment
from flask import Flask, render_template, session, request, make_response
from flask.ext.socketio import SocketIO, emit, join_room, leave_room


####
# User Views
####

@app.route('/', methods=['POST', 'GET'])
def index():
    #TODO: probably should block for admin to start
    #TODO: Build a check to determine if we should resume a disconnected experiment

    # intercept if we think we'll be getting the post with subject information
    if request.method == 'POST':
        subject_id = request.form["subject_id"]
        resp = make_response(render_template("index.html"))
        resp.set_cookie('subject_id', str(subject_id))
        socketio.emit('user_connection', {'connected_user': subject_id}, namespace='/admin_control', broadcast=True)
        return resp

    # our first check is to see if we've got an id associated with the subject
    subject_id = request.cookies.get('subject_id')

    if subject_id is None:
        return render_template('user_signin.html')

    # safety... return the index
    socketio.emit('user_connection', {'signal':'connected','data': subject_id}, namespace='/admin_control')
    return render_template('index.html')



@socketio.on('start_experiment', namespace='/admin_control')
def start_experiment(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    #emit('my response',
    #     {'data': message['data'], 'count': session['receive_count']})
    print "Starting experiment"

@socketio.on('pause_experiment', namespace='/admin_control')
def pause_experiment(message):
    # TODO - Need to create additional logic to maintain experiment pause state
    emit('pause_experiment', {'data': 'pause'}, namespace='/test', broadcast=True)







@socketio.on('my broadcast event', namespace='/admin_control')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/admin_control')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/admin_control')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('my room event', namespace='/admin_control')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace='/admin_control')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})
    emit('my response',
             {'data': "fargiverasfasfasd"},
             namespace='/test', broadcast=True)
    emit('direct_users',
             {'data': "this is a trial balloon"},
             namespace='/test', broadcast=True)
    print experiment.info()


#@socketio.on('disconnect', namespace='/admin_control')
#def test_disconnect():
#    print('Client disconnected')

#
#
#
#


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})
    emit('my response',
             {'data': "fargiverasfasfasd"},
             namespace='/admin_control', broadcast=True)


#@socketio.on('disconnect', namespace='/test')
#def test_disconnect():
#    print('Client disconnected')