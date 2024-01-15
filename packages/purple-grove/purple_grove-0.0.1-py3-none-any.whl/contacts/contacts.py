import logging

import requests


logger = logging.getLogger(__name__)

API_VERSION = 'v0'


class Contacts(object):
    """
    Represents a contact in the system.
    """

    def __init__(self, name=''):
        """
        Params:
        -------
        name: str
            The name of the contact.
        """
        self.name = name
