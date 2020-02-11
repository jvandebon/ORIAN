# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.inline_response2003_config import InlineResponse2003Config  # noqa: F401,E501
from swagger_server.models.tasksexecute_impl import TasksexecuteImpl  # noqa: F401,E501
from swagger_server.models.tasksexecute_input_params import TasksexecuteInputParams  # noqa: F401,E501
from swagger_server import util


class Task1(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, task_name: str=None, input_params: List[TasksexecuteInputParams]=None, config: InlineResponse2003Config=None, impl: TasksexecuteImpl=None, problem_size: int=None, sync: bool=None, profile: bool=None):  # noqa: E501
        """Task1 - a model defined in Swagger

        :param task_name: The task_name of this Task1.  # noqa: E501
        :type task_name: str
        :param input_params: The input_params of this Task1.  # noqa: E501
        :type input_params: List[TasksexecuteInputParams]
        :param config: The config of this Task1.  # noqa: E501
        :type config: InlineResponse2003Config
        :param impl: The impl of this Task1.  # noqa: E501
        :type impl: TasksexecuteImpl
        :param problem_size: The problem_size of this Task1.  # noqa: E501
        :type problem_size: int
        :param sync: The sync of this Task1.  # noqa: E501
        :type sync: bool
        :param profile: The profile of this Task1.  # noqa: E501
        :type profile: bool
        """
        self.swagger_types = {
            'task_name': str,
            'input_params': List[TasksexecuteInputParams],
            'config': InlineResponse2003Config,
            'impl': TasksexecuteImpl,
            'problem_size': int,
            'sync': bool,
            'profile': bool
        }

        self.attribute_map = {
            'task_name': 'taskName',
            'input_params': 'inputParams',
            'config': 'config',
            'impl': 'impl',
            'problem_size': 'problemSize',
            'sync': 'sync',
            'profile': 'profile'
        }

        self._task_name = task_name
        self._input_params = input_params
        self._config = config
        self._impl = impl
        self._problem_size = problem_size
        self._sync = sync
        self._profile = profile

    @classmethod
    def from_dict(cls, dikt) -> 'Task1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The task_1 of this Task1.  # noqa: E501
        :rtype: Task1
        """
        return util.deserialize_model(dikt, cls)

    @property
    def task_name(self) -> str:
        """Gets the task_name of this Task1.


        :return: The task_name of this Task1.
        :rtype: str
        """
        return self._task_name

    @task_name.setter
    def task_name(self, task_name: str):
        """Sets the task_name of this Task1.


        :param task_name: The task_name of this Task1.
        :type task_name: str
        """

        self._task_name = task_name

    @property
    def input_params(self) -> List[TasksexecuteInputParams]:
        """Gets the input_params of this Task1.


        :return: The input_params of this Task1.
        :rtype: List[TasksexecuteInputParams]
        """
        return self._input_params

    @input_params.setter
    def input_params(self, input_params: List[TasksexecuteInputParams]):
        """Sets the input_params of this Task1.


        :param input_params: The input_params of this Task1.
        :type input_params: List[TasksexecuteInputParams]
        """

        self._input_params = input_params

    @property
    def config(self) -> InlineResponse2003Config:
        """Gets the config of this Task1.


        :return: The config of this Task1.
        :rtype: InlineResponse2003Config
        """
        return self._config

    @config.setter
    def config(self, config: InlineResponse2003Config):
        """Sets the config of this Task1.


        :param config: The config of this Task1.
        :type config: InlineResponse2003Config
        """

        self._config = config

    @property
    def impl(self) -> TasksexecuteImpl:
        """Gets the impl of this Task1.


        :return: The impl of this Task1.
        :rtype: TasksexecuteImpl
        """
        return self._impl

    @impl.setter
    def impl(self, impl: TasksexecuteImpl):
        """Sets the impl of this Task1.


        :param impl: The impl of this Task1.
        :type impl: TasksexecuteImpl
        """

        self._impl = impl

    @property
    def problem_size(self) -> int:
        """Gets the problem_size of this Task1.


        :return: The problem_size of this Task1.
        :rtype: int
        """
        return self._problem_size

    @problem_size.setter
    def problem_size(self, problem_size: int):
        """Sets the problem_size of this Task1.


        :param problem_size: The problem_size of this Task1.
        :type problem_size: int
        """

        self._problem_size = problem_size

    @property
    def sync(self) -> bool:
        """Gets the sync of this Task1.


        :return: The sync of this Task1.
        :rtype: bool
        """
        return self._sync

    @sync.setter
    def sync(self, sync: bool):
        """Sets the sync of this Task1.


        :param sync: The sync of this Task1.
        :type sync: bool
        """

        self._sync = sync

    @property
    def profile(self) -> bool:
        """Gets the profile of this Task1.


        :return: The profile of this Task1.
        :rtype: bool
        """
        return self._profile

    @profile.setter
    def profile(self, profile: bool):
        """Sets the profile of this Task1.


        :param profile: The profile of this Task1.
        :type profile: bool
        """

        self._profile = profile
