from flask.ext.script import Shell, Manager

from flask_web import app,create_app
from database import models
from database.models import db
from flask.ext.migrate import Migrate, MigrateCommand
def _make_context():
    return dict(app=app, db=db, models=models)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context,use_ipython=True))
manager.add_command("db",MigrateCommand)
if __name__ == "__main__":
    manager.run()