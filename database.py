from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# connect to the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('PROJECT_MGT_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
API_KEY = os.environ.get('PROJECT_MGT_API_KEY')


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), unique=True, nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    project_done = db.Column(db.Boolean, nullable=False)
    # each project have its set of tasks and teams
    tasks = db.relationship('Tasks', back_populates='project_task')
    teams = db.relationship('Teams', back_populates='project_team')
    member = db.relationship('Member', back_populates='project_member')

    def to_dict(self):
        # create a dictionary
        dictionary = {}
        # loop through each column in a data record
        for column in self.__table__.columns:
            # for each column, the key is the name of the column and the
            # value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(250), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    task_done = db.Column(db.Boolean, nullable=False)
    # FOREIGN KEY ASSIGNMENT
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    # CREATE REFERNCE TO PARENT OBJECT, THROUGH THE todos property
    project_task = db.relationship('Project', back_populates='tasks')
    # each team member has a task assigned to him or her.
    member = db.relationship('Member', back_populates='task')

    def to_dict(self):
        # create a dictionary
        dictionary = {}
        # loop through each column in a data record
        for column in self.__table__.columns:
            # for each column, the key is the name of the column and the
            # value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Teams(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(250), unique=True, nullable=False)
    team_description = db.Column(db.Text, unique=True)
    # FOREIGN KEY ASSIGNMENT
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    # CREATE REFERNCE TO PARENT OBJECT, THROUGH THE todos property
    project_team = db.relationship('Project', back_populates='teams')
    member = db.relationship('Member', back_populates='team_member')

    def to_dict(self):
        # create a dictionary
        dictionary = {}
        # loop through each column in a data record
        for column in self.__table__.columns:
            # for each column, the key is the name of the column and the
            # value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(250), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    team_member = db.relationship('Teams', back_populates='member')
    project_member = db.relationship('Project', back_populates='member')
    task = db.relationship('Tasks', back_populates='member')

    def to_dict(self):
        # create a dictionary
        dictionary = {}
        # loop through each column in a data record
        for column in self.__table__.columns:
            # for each column, the key is the name of the column and the
            # value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


# with app.app_context():
#     # db.drop_all()
#     db.create_all()
