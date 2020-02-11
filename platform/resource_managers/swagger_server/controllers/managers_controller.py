import connexion
import six

from swagger_server.models.child import Child  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util
from flask import current_app

def check_available():
    """ Checks for available resources

     # noqa: E501


    :rtpye: List[objext]
    """

    rm = current_app.config['rm_object']

    return  rm.check_availability()



def register_child_rm(child):  # noqa: E501
    """Registers a new child RM

     # noqa: E501

    :param child: child RM specs
    :type child: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        child = Child.from_dict(connexion.request.get_json())  # noqa: E501
    
    rm = current_app.config['rm_object']
    url = child.url
    rm_type = child.rm_type
    
    return  rm.register_child({'url': url, 'rm_type': rm_type})
