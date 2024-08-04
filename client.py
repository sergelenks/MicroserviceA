import zmq
import json


def send_list_to_sort(tasks, list_name):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Prepare and send the request
    request = {"list_name": list_name, "tasks": tasks}
    print(f"Sending request: {json.dumps(request, indent=2)}")
    socket.send_json(request)

    # Receive and process the response
    response = socket.recv_json()
    print(f"Received response: {json.dumps(response, indent=2)}")

    socket.close()
    return response.get("sorted_list")


# Test data - single list
test_tasks = [
    {"task": "Buy groceries", "due_date": "08/04/24"},
    {"task": "Gym", "due_date": "08/02/24"},
    {"task": "Call mom", "due_date": "08/10/24"},
    {"task": "Finish report", "due_date": "08/05/24"},
    {"task": "Team meeting", "due_date": "08/01/24"}
]

# Test the service
print("Testing Task Sorting Service:")
sorted_lists = send_list_to_sort(test_tasks, "Personal Tasks")

if sorted_lists:
    print("\nSorted by date:")
    for task in sorted_lists["by_date"]:
        print(f"  {task['task']} - {task['due_date']}")

    print("\nSorted alphabetically:")
    for task in sorted_lists["alphabetically"]:
        print(f"  {task['task']} - {task['due_date']}")
else:
    print("No sorted lists returned.")

print("\nTest completed.")