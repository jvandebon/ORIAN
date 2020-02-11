# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class TasksInputParams(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, param: str=None, type: str=None):  # noqa: E501
        """TasksInputParams - a model defined in Swagger

        :param param: The param of this TasksInputParams.  # noqa: E501
        :type param: str
        :param type: The type of this TasksInputParams.  # noqa: E501
        :type type: str
        """
        self.swagger_types = {
            'param': str,
            'type': str
        }

        self.attribute_map = {
            'param': 'param',
            'type': 'type'
        }

        self._param = param
        self._type = type

    @classmethod
    def from_dict(cls, dikt) -> 'TasksInputParams':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The tasks_inputParams of this TasksInputParams.  # noqa: E501
        :rtype: TasksInputParams
        """
        return util.deserialize_model(dikt, cls)

    @property
    def param(self) -> str:
        """Gets the param of this TasksInputParams.


        :return: The param of this TasksInputParams.
        :rtype: str
        """
        return self._param

    @param.setter
    def param(self, param: str):
        """Sets the param of this TasksInputParams.


        :param param: The param of this TasksInputParams.
        :type param: str
        """

        self._param = param

    @property
    def type(self) -> str:
        """Gets the type of this TasksInputParams.


        :return: The type of this TasksInputParams.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this TasksInputParams.


        :param type: The type of this TasksInputParams.
        :type type: str
        """

        self._type = type
