import requests


class ServiceHandler:
    endpoint = ""
    payload = {}

    def get(self, **kwargs):
        req = requests.get(self.endpoint, params=self.payload)
        return req.json()


class ClassServiceHandler(ServiceHandler):
    endpoint = "http://localhost:12300/api/class"

    def __init__(self, **kwargs):
        classcode = kwargs.get('classcode')
        self.endpoint = f"{self.endpoint}/{classcode}"

class TaskServiceHandler(ServiceHandler):
    endpoint = "http://localhost:12302/api/tasks"

    def __init__(self, **kwargs):
        self.endpoint = f"{self.endpoint}"

class SingleTaskServiceHandler(ServiceHandler):
    endpoint = "http://localhost:12302/api/task"

    def __init__(self, **kwargs):
        id = kwargs.get('taskid')
        self.endpoint = f"{self.endpoint}/{id}"

if __name__ == "__main__":
    #csh = ClassServiceHandler(classcode="21E1_1")
    csh = TaskServiceHandler()
    print(csh.get())
