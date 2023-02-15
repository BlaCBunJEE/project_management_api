from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from database import Project, Teams, Tasks, Member

app = Flask(__name__)
db = SQLAlchemy(app)


# API DESIGN STARTS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def get_all_projects():
    all_projects = db.session.query(Project).all()
    return jsonify(all_projects=[project.to_dict() for project in all_projects])
    # return jsonify({'response': 'testing'})


@app.route('/search_project')
def get_project():
    query_project = request.args.get('p_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    if project:
        return jsonify(project=project.to_dict())
    else:
        return jsonify(error={"Not Found": "Project you are looking for could not be found."})


@app.route('/add_project', methods=['POST'])
def new_project():
    try:
        create_project = Project(
            project_name=request.form.get('p_name'),
            project_description=request.form.get('desc'),
            project_done=bool(request.form.get('done'))
        )
        db.session.add(create_project)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(response={'Error': 'Unable to add new project.'})
    else:
        return jsonify(response={'Success': 'Successfully added a new project.'})


@app.route('/delete_project', methods=['DELETE'])
def project_delete():
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        query_project = request.form.get('p_name')
        project = db.session.query(Project).filter_by(project_name=query_project).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify(response={'Success': 'Successfully deleted the project.'}), 200
        else:
            return jsonify(response={'Not found': 'Project you are looking for could not be found.'}), 404
    else:
        return jsonify(error={'Error': 'You have put in an incorrect key. Make sure you have the correct key.'}), 403


@app.route('/new_member', methods=['POST'])
def add_new_member():
    query_project = request.form.get('p_name')
    # query_team = request.form.get('team_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    # team = db.session.query(Teams).filter_by(team_name=query_team).first()
    if project:
        new_member = Member(
            first_name=request.form.get('fname'),
            last_name=request.form.get('lname'),
            email=request.form.get('email'),
            password=request.form.get('password'),
            skills=request.form.get('skills'),
            # team_id=team.id,
            project_id=project.id
        )
        db.session.add(new_member)
        db.session.commit()
        return jsonify(response={'Success': 'Your new member has been added to the project.'}), 200
    else:
        return jsonify(response={'Error': 'Your new member could not be added to the project.'})


@app.route('/create_new_team', methods=['POST'])
def new_team():
    query_project = request.form.get('p_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    if project:
        add_team = Teams(
            team_name=request.form.get('team_name'),
            team_description=request.form.get('team_desc'),
            project_id=project.id
        )
        db.session.add(add_team)
        db.session.commit()
        return jsonify(response={'Success': 'Your new team has been created.'}), 200
    else:
        return jsonify(response={'Error': 'Your new team could not be created.'})


@app.route('/assign_to_team', methods=['PATCH'])
def assign_members_to_teams():
    query_team = request.form.get('team_name')
    team = db.session.query(Teams).filter_by(team_name=query_team).first()
    query_member = request.form.get('email')
    member = db.session.query(Member).filter_by(email=query_member).first()
    if team and member:
        member.team_id = team.id
        db.session.commit()
        return jsonify(response={
            'Success': f'Successfully assigned {member.first_name.title()} to {team.team_name.title()} team'}), 200
    else:
        return jsonify(error={'Error': f'{member.first_name} could not be assigned'})


@app.route('/all_project_teams')
def all_teams():
    query_project = request.form.get('p_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    all_assigned_teams = db.session.query(Teams).filter_by(project_id=project.id).all()
    return jsonify(all_teams=[team.to_dict() for team in all_assigned_teams])


@app.route('/delete_team', methods=['DELETE'])
def delete_team():
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        query_team = request.form.get('team_name')
        team = db.session.query(Teams).filter_by(team_name=query_team).first()
        if team:
            db.session.delete(team)
            db.session.commit()
            return jsonify(response={'Success': 'Successfully deleted the team.'}), 200
        else:
            return jsonify(response={'Not found': 'Team you are looking has not been created.'}), 404
    else:
        return jsonify(error={'Error': 'You have put in an incorrect key. Make sure you have the correct key.'}), 403


@app.route('/add_task', methods=['POST'])
def new_task():
    query_project = request.form.get('p_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    if project:
        added_task = Tasks(
            task_name=request.form.get('task_name'),
            task_description=request.form.get('task_desc'),
            task_done=bool(request.form.get('task_done')),
            project_id=project.id
        )
        db.session.add(added_task)
        db.session.commit()
        return jsonify(response={'Success': 'Your new task has been created.'}), 200
    else:
        return jsonify(response={'Error': 'Your new task could not be created.'})


@app.route('/task_asign', methods=['PATCH'])
def assign_task_to_member():
    query_task = request.form.get('task_name')
    task = db.session.query(Teams).filter_by(task_name=query_task).first()
    query_member = request.form.get('email')
    member = db.session.query(Member).filter_by(email=query_member).first()
    if task and member:
        member.task_id = task.id
        db.session.commit()
        return jsonify(response={'Success': f'Task has been assigned to {member.first_name.title()}'})
    else:
        return jsonify(response={'Error': f'{member.first_name.title()} could not be '})


@app.route('/all_tasks')
def get_all_tasks():
    query_project = request.form.get('p_name')
    project = db.session.query(Project).filter_by(project_name=query_project).first()
    all_assigned_tasks = db.session.query(Tasks).filter_by(project_id=project.id).all()
    return jsonify(all_tasks=[tasks.to_dict() for tasks in all_assigned_tasks])


@app.route('/delete_task', methods=['DELETE'])
def delete_task():
    api_key = request.args.get('api-key')
    if api_key == API_KEY:
        query_task = request.form.get('task_name')
        task = db.session.query(Tasks).filter_by(task_name=query_task).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            return jsonify(response={'Success': 'Successfully deleted the task.'}), 200
        else:
            return jsonify(response={'Not found': 'Task you are looking has not been assigned.'}), 404
    else:
        return jsonify(error={'Error': 'You have put in an incorrect key. Make sure you have the correct key.'}), 403


if __name__ == "__main__":
    app.run(debug=True)
