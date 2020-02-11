# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.models.task import Task  # noqa: E501
from swagger_server.models.task1 import Task1  # noqa: E501
from swagger_server.test import BaseTestCase


class TestTasksController(BaseTestCase):
    """TasksController integration test stubs"""

    def test_execute(self):
        """Test case for execute

        Executes a task
        """
        task = Task()
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/tasks/execute',
            method='POST',
            data=json.dumps(task),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_tasks(self):
        """Test case for get_tasks

        Returns all supported tasks
        """
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/tasks',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_optimal_config(self):
        """Test case for optimal_config

        Returns optimal configuration
        """
        task = Task1()
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/tasks/config',
            method='GET',
            data=json.dumps(task),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
