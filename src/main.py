import time
from phue import Bridge
from light_controller import LightController
from vlc_tracker import VLCTracker
BRIDGE_IP = '192.168.0.30'
GROUP_NAME = 'Bedroom'

def react_to_vlc():
    v = VLCTracker('','password')
    b = Bridge(BRIDGE_IP)
    b.connect()
    outcome = ''
    while True:
        new_outcome = v.get_state()
        if outcome != new_outcome:
            # Something changed
            if new_outcome == 'playing':
                # Turn off lights
                b.set_group(1, 'on', False)
            elif new_outcome == 'paused':
                # Dim lights
                b.set_group(1, 'on', True)
            else:
                # Restore light
                b.set_group(1, 'on', True)
            print("State changed from '" + outcome + "' to '" + new_outcome + "'")
        else:
            pass
        outcome = new_outcome
        time.sleep(0.1)


if __name__ == "__main__":
    b = Bridge(BRIDGE_IP)
    b.connect()
    lc = LightController(b, GROUP_NAME)
    print("Saving State")
    lc.save_state()
    print("Turning off the lights")
    b.set_group(1, 'on', False)
    time.sleep(5)
    lc.restore()