from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from configs.DBConfig import DevelopmentConfigs

app = Flask(__name__)
app.config.from_object(DevelopmentConfigs)
api = Api(app, title='Task management api', description='task manager api', version='1.0', author='Ian')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# models
from models.TaskModel import TaskModel
from models.UserModel import UserModel


@app.before_first_request
def create_tables():
    db.create_all()


from resources.Task import *
from resources.User import *

if __name__ == '__main__':
    app.run()
