from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import socketio


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = 'Room'
    join_room(room)
    usr = current_user._get_current_object()
    emit('status', {'msg': usr.username + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    usr = current_user._get_current_object()
    emit('message', {'msg': usr.username + ': ' + message['msg']}, room='Room')


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = ' Room'
    leave_room(room)
    usr = current_user._get_current_object()
    emit('status', {'msg': usr.username + ' has left the room.'}, room=room)
