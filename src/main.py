import time
from phue import Bridge
from light_controller import LightController
BRIDGE_IP = '192.168.0.30'
GROUP_NAME = 'Bedroom'

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