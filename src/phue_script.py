#] /usr/bin/env python
import time
BRIDGE_IP = '192.168.0.30'
GROUP_NAME = 'Bedroom'

from phue import Bridge

def get_light_state(light):
    command = {
        'transitiontime': light.transitiontime,
        'on': light.on,
        'effect': light.effect,
        'saturation': light.saturation,
        'brightness': light.brightness,
        'xy': light.xy
    }
    return command
bridge = Bridge(BRIDGE_IP)
bridge.connect()
GROUP_ID = bridge.get_group_id_by_name(GROUP_NAME)

bedroom_light_ids = bridge.get_group(GROUP_NAME,'lights')
lights = bridge.get_light_objects('id')
print("Getting Lights")
backup_lights = []
for x in bedroom_light_ids:
    light_id = int(x)
    id_command = (light_id, get_light_state(lights[light_id]))
    print("Backing up: " + str(light_id))
    backup_lights.append(id_command)
time.sleep(1)
print("Turning off lights")
bridge.set_group(1, 'on', False)
time.sleep(3)
print("Restoring lights")
for id, command in backup_lights:
    bridge.set_light(id, command)


