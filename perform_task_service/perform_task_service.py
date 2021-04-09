import os.path
from config import app, ma, db, database_file, project_dir
from flask import jsonify, render_template, request

from marshmallow_enum import EnumField
from dateutil import parser

# TODO: Develop a independent python module
# TODO: Probably better to develop a Event Bus
import sys
sys.path.insert(1, f"{project_dir}/../services/")
sys.path.insert(2, f"{project_dir}/../tasks_service/")
sys.path.insert(3, f"{project_dir}/../perform_task_service/")
from tasks_service import Tarefas, TasksSchema
from ServiceMapping import TaskServiceHandler, SingleTaskServiceHandler
####

task_schema = TasksSchema()
all_task_schema = TasksSchema(many = True)


@app.route("/home", methods=["GET"])
def home2():
    tasks = TaskServiceHandler().get()
    #tasks = _tasks.get()

    return render_template("perform_tasks.html",
                           tasks=tasks)

@app.route("/accomplished/", methods=["POST"])
def accomplished():
    taskid = request.form["taskid"]
    _task = SingleTaskServiceHandler(taskid=taskid).get()

    _task['done'] = 1
    db.session.commit()
    result = SingleTaskServiceHandler(taskid=taskid).get()
    return jsonify(all_task_schema.dump(result))


if __name__ == "__main__":
    if not os.path.exists(database_file):
        db.create_all()
    app.run(host="0.0.0.0", port=12303)