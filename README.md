# Task Sorting Microservice

This microservice provides task sorting functionality using ZeroMQ for communication.

## Communication Contract

To request data from the microservice:

1. Ensure you have ZeroMQ installed: `pip install pyzmq`
2. Use a ZeroMQ REQ socket to connect to the service
3. Send a JSON-formatted message with the following structure:

```python
{
    "list_name": "Your List Name",
    "tasks": [
        {"task": "Task description", "due_date": "MM/DD/YY"},
    ]
}

Example call:

import zmq
import json

def request_sorted_tasks(tasks, list_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    request = {
        "list_name": list_name,
        "tasks": tasks
    }
    socket.send_json(request)

    return socket.recv_json()

# Example usage
tasks = [
    {"task": "Buy groceries", "due_date": "08/04/24"},
    {"task": "Gym", "due_date": "08/02/24"},
    {"task": "Call mom", "due_date": "08/10/24"}
]

response = request_sorted_tasks(tasks, "Personal Tasks")

-----------------------------------------------------------------------------------
To receive data from the microservice:

1. Use the recv_json() method on your ZeroMQ socket to get the response
2. Parse the JSON response to access the sorted lists

Example call:

response = socket.recv_json()
sorted_by_date = response["sorted_list"]["by_date"]
sorted_alphabetically = response["sorted_list"]["alphabetically"]

print("Sorted by date:")
for task in sorted_by_date:
    print(f"{task['task']} - {task['due_date']}")

print("\nSorted alphabetically:")
for task in sorted_alphabetically:
    print(f"{task['task']} - {task['due_date']}")

The microservice will respond with a JSON-formatted message containing the sorted tasks:

{
    "sorted_list": {
        "by_date": [
            {"task": "Task description", "due_date": "MM/DD/YY"},
        ],
        "alphabetically": [
            {"task": "Task description", "due_date": "MM/DD/YY"},
        ]
    }
}


