import connexion
import six

from swagger_server.models.task2 import Task2  # noqa: E501
from swagger_server import util
from flask import current_app

def build_model(task):  # noqa: E501
    """Builds a performance model

     # noqa: E501

    :param task: Task (and implentation) to build model for
    :type task: dict | bytes

    :rtype: None
    """

    if connexion.request.is_json:
        json_task = connexion.request.get_json()
        task = Task2.from_dict(connexion.request.get_json())  # noqa: E501
    
    rm = current_app.config['rm_object']

    task_name = json_task['taskName']
    impl_name = json_task['implName']
    return rm.build_model(task_name, impl_name)


def get_models():  # noqa: E501
    """Returns all performance models

     # noqa: E501


    :rtype: List[object]
    """
    rm = current_app.config['rm_object']
    return rm.get_models()
