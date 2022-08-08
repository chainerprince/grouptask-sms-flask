from smsapp import create_app, db, socketio
from smsapp.models import User, Chat
from flask_migrate import Migrate

app = create_app('default')
migrate = Migrate(app, db=db)


# Make shell context processor
@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Chat=Chat)


if __name__ == "__main__":
    socketio.run(app, debug=True) 