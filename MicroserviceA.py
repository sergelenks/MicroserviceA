import zmq
import json
from operator import itemgetter
from datetime import datetime

class TaskSorter:
    def __init__(self):
        pass

    def sort_by_due_date(self, tasks):
        return sorted(tasks, key=lambda x: datetime.strptime(x['due_date'], '%m/%d/%y'))

    def sort_alphabetically(self, tasks):
        return sorted(tasks, key=itemgetter('task'))

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

task_sorter = TaskSorter()

print("Task Sorting Service is running...")

while True:
    message = socket.recv_json()
    list_name = message.get("list_name")
    tasks = message.get("tasks")

    if not tasks:
        response = {"error": "No tasks provided"}
    else:
        sorted_by_date = task_sorter.sort_by_due_date(tasks)
        sorted_alphabetically = task_sorter.sort_alphabetically(tasks)

        response = {
            "sorted_list": {
                "by_date": sorted_by_date,
                "alphabetically": sorted_alphabetically
            }
        }

    socket.send_json(response)
    print(f"Processed request for list: {list_name}")