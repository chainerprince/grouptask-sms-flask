from smsapp import create_app, db
from flask_migrate import Migrate
from smsapp.models import Chat, User

app = create_app('default')
migrate = Migrate(app, db)


# Make shell context processor
@app.shell_context_processor
def make_shell_context():
    return dict(User=User, Chat=Chat)


if __name__ == "__main__":
    app.run(debug=True)