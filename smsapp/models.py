from smsapp import db, login_manager
from flask_login import UserMixin
import json

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(int(user_id))


# Create User models
class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True, index=True, nullable=False)
    password = db.Column(db.String(150))
    image = db.Column(db.String(50), default='default.jpg')
    
    
    
    def __str__(self):
        return f"User {self.username}"
    
    
class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)    


# Create Chat Model
class Chat(db.Model):
    __tablename__ = "chats"
    
    
    id = db.Column(db.Integer, primary_key=True)
    recepient = db.Column(db.String(80))
    chat_details = db.Column(JsonEncodedDict)
    room_id = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('chat_list', lazy=True))
    
    def __str__(self):
        return f"Chat {self.id}"