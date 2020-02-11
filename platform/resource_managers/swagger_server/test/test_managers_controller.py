# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.child import Child  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.test import BaseTestCase


class TestManagersController(BaseTestCase):
    """ManagersController integration test stubs"""

    def test_register_child_rm(self):
        """Test case for register_child_rm

        Registers a new child RM
        """
        child = Child()
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/managers/register',
            method='PUT',
            data=json.dumps(child),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
