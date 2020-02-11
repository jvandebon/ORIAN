import connexion
import six

from swagger_server import util
from flask import current_app

def get_impls():  # noqa: E501
    """Returns all supported impls

     # noqa: E501


    :rtype: List[object]
    """
    rm = current_app.config['rm_object']
    return rm.get_impls()