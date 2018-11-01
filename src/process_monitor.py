#! /usr/bin/env python
import os
import time

class ProcessMonitor(object):
    """
    Monitor the running state of a particular process
    """
    def __init__(self, process_name):
        self.process_name = process_name
        self._command = "ps -A | grep '{0}' | grep -v 'grep' | awk '{{ print $4 }}'"

    def block_until_process_detected(self, polling_rate=1):
        """
        Blocking call until the process is detected.
        :param double polling_rate: How many times per second to check
        :returns bool: Returns True when process is detected
        """
        # Timeout can be added in the future if necessary 
        sleep_duration = 1 / polling_rate
        while not self._process_exists(self.process_name):
            time.sleep(sleep_duration)
        return True

    def is_running(self):
        """
        Quickly check if the process is running
        :returns bool:
        """
        return self._process_exists(self.process_name)

    def _process_exists(self, process_name):
        """
        Check that a process is running on the system
        :param str process_name" Name of the process to look for
        :returns bool: True if matching process is found
        """
        output = os.popen(self._command.format(process_name)).read().strip()
        return output == process_name