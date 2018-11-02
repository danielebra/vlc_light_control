#! /usr/bin/env python
from phue import Bridge

class LightController(object):
    def __init__(self, bridge, group_name):
        self._bridge = bridge
        self._group_name = group_name
        self._light_backups = []
        self._light_objects = self._bridge.get_light_objects('id')
        self._light_ids = self._bridge.get_group(self._group_name, 'lights')
        self._group_id = int(self._bridge.get_group_id_by_name(group_name))

    def turn_off(self):
        """Turn off the lights"""
        self._bridge.set_group(self._group_id, 'on', False)

    def ambient_lighting(self):
        """Set the lights to a low yellow light"""
        self._bridge.set_group(self._group_id, self._ambient_light_command())

    def restore(self):
        """Restore the lights to their previously saved values"""
        for id, command in self._light_backups:
            self._bridge.set_light(id, command)

    def save_state(self):
        """Save the current state of the lights"""
        self._light_backups = []
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
            'sat': light.saturation,
            'bri': light.brightness,
            'xy': light.xy
        }
        return command
    def _ambient_light_command(self):
        command = {
            'on': True,
            'bri': 30,
            'ct': 450
        }
        return command