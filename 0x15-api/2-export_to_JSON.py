#!/usr/bin/python3
"""
Python script to export data in JSON format based on employee ID.
"""

import json
import requests
from sys import argv


def fetch_employee_data(employee_id):
    """
    Fetches employee data from the REST API.
    """
    base_url = 'https://jsonplaceholder.typicode.com/'
    user_url = base_url + 'users/{}'.format(employee_id)
    todo_url = base_url + 'todos?userId={}'.format(employee_id)

    try:
        user_response = requests.get(user_url)
        todo_response = requests.get(todo_url)
        user_data = user_response.json()
        todo_data = todo_response.json()
    except Exception as e:
        print("Error:", e)
        return None, None

    return user_data, todo_data


def export_to_json(user_data, todo_data):
    """
    Exports employee TODO list data to JSON file.
    """
    if not user_data or not todo_data:
        print("Employee data not found.")
        return

    employee_id = user_data.get('id')
    employee_name = user_data.get('name')
    if not employee_id or not employee_name:
        print("Employee information incomplete.")
        return

    json_data = {str(employee_id): []}
    for task in todo_data:
        json_data[str(employee_id)].append({
            "task": task['title'],
            "completed": task['completed'],
            "username": employee_name
        })

    json_file = '{}.json'.format(employee_id)
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)
    print("Data exported to", json_file)


if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: {} <employee_id>".format(argv[0]))
        exit(1)

    employee_id = argv[1]
    user_data, todo_data = fetch_employee_data(employee_id)
    export_to_json(user_data, todo_data)

