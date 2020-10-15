from datetime import datetime
from app import db

from hashlib import sha256

########################################
#  You do not need to touch this file  #
########################################

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(10), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True)
    content = db.Column(db.String(120))

    def __repr__(self):
        return '<Message {} from {}'.format(self.id, self.chat_id)

    def to_dict(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "timestamp": str(self.timestamp),
            "username": self.username,
            "content": self.content
        }


class MessageManager:

    @staticmethod
    def get_all_messages():
        return Message.query.all()

    @staticmethod
    def get_message_by_id(message_id):
        return Message.query.get(message_id)

    @staticmethod
    def filter_messages_by_chat_id(chat_id):
        return Message.query.filter(Message.chat_id == chat_id)

    @staticmethod
    def get_last_messages(num_messages):
        return Message.query.order_by(Message.timestamp.desc()).limit(num_messages)

    @staticmethod
    def get_last_messages_in_chat(chat_id, num_messages):
        return Message.query.filter(Message.chat_id == chat_id).order_by(Message.timestamp.asc()).limit(num_messages)
    
    @staticmethod
    def get_message_updates_in_chat(chat_id, last_id):
        return Message.query.filter(Message.chat_id == chat_id).filter(Message.id > last_id).order_by(Message.timestamp.asc())

    @staticmethod
    def create_message(message_dict):
        message_username = message_dict.get('username', "")
        message_content = message_dict.get('content', "")
        message_chat_id = message_dict.get('chat_id', "")
        message = Message(
            username=message_username,
            content=message_content,
            chat_id=message_chat_id
        )
        db.session.add(message)
        db.session.commit()
        return message

    @staticmethod
    def delete_message(message_id):
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
        else:
            raise ValueError(
                "Could not find Message with ID: " + str(message_id)
            )
        return True

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(16), index=True)
    username = db.Column(db.String(64), index=True)

    def __repr__(self):
        return '<Session {} for: {}'.format(self.token, self.username)

class SessionManager:

    @staticmethod
    def create_session(username):
        token = sha256(str(datetime.now()).encode('utf-8')).hexdigest()[:16]
        session = Session(
            token=token,
            username=username
        )
        db.session.add(session)
        db.session.commit()
        return token

    @staticmethod
    def get_username(token):
        session = Session.query.filter(Session.token == token).first()
        return session.username
    