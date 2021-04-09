import os
from config import app, db, ma, database_name, project_dir
from school_class import Student, Class
import sys
sys.path.insert(2, f"{project_dir}/../tasks_service/")
from tasks_service import Tarefas

# Data to initialize database with
STUDENTS = [
    {'name': "Albert Einsten", 'email': "albert.einstein@al.infnet.edu.br"},
    {'name': "Marie Curie", 'email': "marie.curie@al.infnet.edu.br"},
    {'name': "Nicolas Tesla", 'email': "nicolas.tesla@al.infnet.edu.br"}
]

CLASSES = [
        {'classcode': "21E1_1", 'classname': "Desenvolvimento de Software Ágil e Escalável com Microsserviços"}
]

TASKS = []#{'classcode': "21E1_1", 'classname': "Desenvolvimento de Software Ágil e Escalável com Microsserviços", 'task_name': "Teste", 'progress': "N"}
    

if os.path.exists(database_name):
    os.remove(database_name)

#db.drop_all()
db.create_all()

for _class in CLASSES:
    class_obj = Class(**_class)
    db.session.add(class_obj)

for student in STUDENTS:
    student_obj = Student(**student)
    student_obj.classes.append(class_obj)
    db.session.add(student_obj)

#for task in TASKS:
#    task_obj = Tarefas(**task)
#    db.session.add(task_obj)

db.session.commit()
