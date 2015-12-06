#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: yuandunlong
# @Date:   2015-09-18 10:04:17
# @Last Modified by:   yuandunlong
# @Last Modified time: 2015-11-18 17:50:38
# -*- coding: utf-8 -*-
from flask_script import Shell, Manager

from flask_web import app,create_app
from database import models
from database.models import db
from flask_migrate import Migrate, MigrateCommand
from flask import current_app
def _make_context():
    return dict(app=app, db=db, models=models,current_app=current_app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("shell", Shell(make_context=_make_context,use_ipython=True))
manager.add_command("db",MigrateCommand)
if __name__ == "__main__":
    manager.run()