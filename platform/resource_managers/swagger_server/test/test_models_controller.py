# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.task2 import Task2  # noqa: E501
from swagger_server.test import BaseTestCase


class TestModelsController(BaseTestCase):
    """ModelsController integration test stubs"""

    def test_build_model(self):
        """Test case for build_model

        Builds a performance model
        """
        task = Task2()
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/models/build',
            method='POST',
            data=json.dumps(task),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_models(self):
        """Test case for get_models

        Returns all performance models
        """
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/models',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
