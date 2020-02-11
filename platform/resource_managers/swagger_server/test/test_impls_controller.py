# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestImplsController(BaseTestCase):
    """ImplsController integration test stubs"""

    def test_get_impls(self):
        """Test case for get_impls

        Returns all supported impls
        """
        response = self.client.open(
            '/jvandebon/rm_prototype/1.0/impls',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
