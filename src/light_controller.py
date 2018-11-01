#! /usr/bin/env python
from phue import Bridge

class LightController(object):
    def __init__(self, bridge, group_name):
        self._bridge = bridge
        self._group_name = group_name
        self._light_backups = []
        self._light_objects = self._bridge.get_light_objects('id')
        self._light_ids = self._bridge.get_group(self._group_name, 'lights')
    def restore(self):
        """ Restore the lights to their previously saved values """
        for id, command in self._light_backups:
            self._bridge.set_light(id, command)

    def save_state(self):
        """Save the current state of the lights"""
        for x in self._light_ids:
            light_id = int(x)
            command = self._convert_light_to_command(self._light_objects[light_id])
            self._light_backups.append((light_id, command))
    
    def _convert_light_to_command(self, light):
        """
        Converts a light to a command
        :param light: Light object
        :returns dict: Dictionary of light property values
        """
        command = {
            'transitiontime': light.transitiontime,
            'on': light.on,
            'effect': light.effect,
            'saturation': light.saturation,
            'brightness': light.brightness,
            'xy': light.xy
        }
        return command