import connexion
import six

from swagger_server.models.inline_response2003 import InlineResponse2003  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server.models.task1 import Task1  # noqa: E501
from swagger_server import util
from flask import current_app

def execute(task):  # noqa: E501
    """Executes a task

     # noqa: E501

    :param task: Function to execute with configuration
    :type task: dict | bytes

    :rtype: object
    """
    if connexion.request.is_json:
        json_task = connexion.request.get_json()
    
    rm = current_app.config['rm_object']

    task_name = json_task['taskName']
    input_params = json_task['inputParams']
    config = json_task['config'] 
    profile = json_task['profile']
    problem_size = json_task['problemSize']
#    impl = json_task['impl']
    sync = json_task['sync']

    return rm.execute(task_name, input_params, config, problem_size, sync, profile)


def get_tasks():  # noqa: E501
    """Returns all supported tasks

     # noqa: E501


    :rtype: List[object]
    """
    rm = current_app.config['rm_object']
    return rm.get_tasks()


def optimal_config(task):  # noqa: E501
    """Returns optimal configuration

     # noqa: E501

    :param task: Function to be executed with input parameters and objectives
    :type task: dict | bytes

    :rtype: InlineResponse2002
    """
    if connexion.request.is_json:
        json_task = connexion.request.get_json()
        task = Task1.from_dict(connexion.request.get_json())  # noqa: E501

        rm = current_app.config['rm_object']

        print(json_task)

        task_name = json_task['taskName']
        objectives = json_task['objectives']
        problem_size = json_task['problemSize']

        return rm.optimal_config(task_name, objectives, problem_size)
