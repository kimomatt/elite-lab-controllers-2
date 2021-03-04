import sys
from app import app
from flask import abort, request, render_template, Response, redirect

from .forms import SessionForm
from .models import MessageManager, SessionManager


# ------------ Web Routes ------------ #

@app.route('/')
@app.route('/index')
def index():
    session_token = request.args.get('token', default=None)
    if session_token:
        return render_template('index.html')
    else:
        return redirect('/session')

@app.route('/session', methods=['GET', 'POST'])
def create_session():
    form = SessionForm()
    if form.validate_on_submit():
        token = SessionManager.create_session(form.username.data)
        return redirect('/index?token=' + token)
    return render_template('session.html', title='Session', form=form)


# ------------ Ajax Routes ------------ #

@app.route('/session/<string:token>/username/', methods=['GET'])
def get_username_from_token(token):
    username = SessionManager.get_username(token)
    return {"username": username}
@app.route('/chat/<string:chat_id>/last', methods=['GET'])
def get_last_messages_in_chat(chat_id):
    count = request.args.get('count', default=100)
    result = MessageManager.get_last_messages_in_chat(chat_id, count)
    response = []
    for message in result:
            response.append(message.to_dict())
    return{"messages": response}

@app.route('/messages/', methods=['POST'])
def create_message():
    body = request.json
    message = MessageManager.create_message(body)
    return {"id": message.id}

@app.route('/chat/<string:chat_id>/updates', methods=['GET'])
def get_chat_updates(chat_id):
    last_id = request.args.get('ref_id', default=0)
    response = []
    result = MessageManager.get_message_updates_in_chat(chat_id, last_id)
    for message in result:
            response.append(message.to_dict())
    return{"messages": response}
