#! /usr/bin/env python

import requests

from xml.dom import minidom

class VLCTracker(object):
    STATE_STOPPED = 'stopped'
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'
    def __init__(self, username, password, link='http://localhost:8080/requests/status.xml'):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self._status_url = link

    def get_state(self):
        return self._get_state_from_status(self._get_status())

    def _get_status(self):
        """
        Get the status of vlc via HTTP interface
        :returns str: Web contents of status.xml
        """
        return self.session.get(self._status_url).content

    def _get_state_from_status(self, xml_str):
        """
        Get the state value from a provided xml tree
        :param str xml_str: A string representation of an xml tree
        :returns str: State outcome (stopped, playing, paused)
        """
        xml_tree = minidom.parseString(xml_str)
        state = xml_tree.getElementsByTagName('state')
        if state:
            state = state[0]
        else:
            raise Exception("Error getting state")

        return str(state.firstChild.nodeValue)

