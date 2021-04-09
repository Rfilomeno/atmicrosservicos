import os.path
from config import app, db, ma, database_file, project_dir
from flask import jsonify, render_template, request

from enum import Enum
from marshmallow_enum import EnumField
from dateutil import parser

# TODO: Develop a independent python module
# TODO: Probably better to develop a Event Bus
import sys
sys.path.insert(1, f"{project_dir}/../services/")
sys.path.insert(2, f"{project_dir}/../tasks_service/")
from ServiceMapping import ClassServiceHandler
####


# Models
class TaskEnum(Enum):
    finished = "F"
    partial = "P"
    notfinished = "N"
    

class Tarefas(db.Model):
    __tablename__ = "tasks3"
    id = db.Column(db.Integer, primary_key=True)
    classcode = db.Column(db.String(256), nullable=True)
    classname = db.Column(db.String(256), nullable=True)
    student_name = db.Column(db.String(256), nullable=True)
    student_id = db.Column(db.Integer(), nullable=True)
    task_name = db.Column(db.String(256), nullable=True)
    done = db.Column(db.Boolean(), default=False) 
    finished = db.Column(db.Boolean(), default=False)    

class TasksSchema(ma.SQLAlchemyAutoSchema):
    presence = EnumField(TaskEnum, by_value=True)
    class Meta:
        model = Tarefas
        fields = ["id", "student_name", "student_id", "task_name", "done", "finished"]

task_schema = TasksSchema()
all_task_schema = TasksSchema(many = True)

@app.route("/", methods=["GET"])
def home1():
    return render_template("task.html")

@app.route("/task/", methods=["POST"])
def take_task():
    classcode = request.form["classcode"]
    taskname = request.form["taskname"]

    _class = ClassServiceHandler(classcode=classcode).get()
    classname = _class.get('classname')
    students = _class.get('students')

    for s in students:
        new_data = {
        "classcode" : request.form["classcode"],
        "classname" : classname,
        "student_name" : s["name"],
        "student_id" : int(s["id"]),
        "task_name" : request.form["taskname"],
        "done" : False,
        "finished" : False
        }
        task = Tarefas(**new_data)
        db.session.add(task)
        db.session.commit()

    result = Tarefas.query.all()
    return jsonify(all_task_schema.dump(result))

@app.route("/api/task/<task_id>", methods=["GET"])
def task_by_id(task_id):
    result = Tarefas.query.get(task_id)
    return task_schema.jsonify(result)


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    result = Tarefas.query.all()
    return jsonify(all_task_schema.dump(result))

if __name__ == "__main__":
    if not os.path.exists(database_file):
        db.create_all()
    app.run(host="0.0.0.0", port=12302)