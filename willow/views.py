from willow import app, socketio, experiment
from flask import Flask, render_template, session, request, make_response
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
import jinja2

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
        experiment.subject_connected(subject_id)
        resp = make_response(render_template("index.html", subject_id = subject_id))
        resp.set_cookie('subject_id', str(subject_id))
        socketio.emit('user_connection', {'signal':'connected','data': subject_id}, namespace='/admin_control')
        return resp

    # our first check is to see if we've got an id associated with the subject
    subject_id = request.cookies.get('subject_id')

    if subject_id is None:
        return render_template('user_signin.html')

    # safety... return the index
    socketio.emit('user_connection', {'signal':'connected','data': subject_id}, namespace='/admin_control')

    experiment.subject_connected(subject_id)

    # since the index is the page we'll be operating through, we'll pass the subject_id to be configured in javascript
    return render_template("index.html", subject_id = subject_id)



@socketio.on('start_experiment', namespace='/admin_control')
def start_experiment(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    #emit('my response',
    #     {'data': message['data'], 'count': session['receive_count']})

    # before starting, check to make sure it's not already in a run state
    if not(experiment.is_running):
        experiment.start_experiment()
        print "Starting experiment"

        # TODO: Here we can start by indicating what round and stage we'll be at in the experiment
        emit('start_experiment', {'data': 'initialize_experiment_window'}, namespace='/subject_space', broadcast=True)



        print "endgame..."

#    template = jinja2.Template('Hello {{ name }}!')
#    template.render(name='John Doe')
#    name = "tester..."
#    return render_template(template, name="tesges")




@socketio.on('pause_experiment', namespace='/admin_control')
def pause_experiment(message):
    # TODO - Need to create additional logic to maintain experiment pause state
    experiment_paused = experiment.pause_experiment()
    if experiment_paused:
        emit('pause_experiment', {'data': 'pause'}, namespace='/subject_space', broadcast=True)
    else:
        emit('pause_experiment', {'data': 'continue'}, namespace='/subject_space', broadcast=True)

@socketio.on('initialize_experiment_window', namespace='/subject_space')
def initialize_experiment_window(message):
    subject_id = message['subject_id']
    rendered_template = experiment.prepare_stage_for_subject(subject_id)
    emit('present_stage_screen', {'stage_screen': rendered_template})
    print "somewhere in here..."


@socketio.on('interface_action', namespace='/subject_space')
def interface_action(message):
    print "received a message"
    emit('interface_message',
         {'data': "testing this out..."})



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