import time
from phue import Bridge
from light_controller import LightController
from vlc_tracker import VLCTracker
from process_monitor import ProcessMonitor
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

class VLCLightControl(object):
    def __init__(self, bridge_ip, group_name, username='', password=''):
        self.bridge = None
        self.light_controller = None
        self._bridge_ip = bridge_ip
        self._group_name = group_name
        self.process_monitor = ProcessMonitor("vlc")
        self.vlc_tracker = VLCTracker(username, password)

        self._vlc_state_previous = None
        self._vlc_state_now = None

    def setup(self):
        self.bridge = Bridge(self._bridge_ip)
        self.bridge.connect()
        time.sleep(0.250)
        self.light_controller = LightController(self.bridge, self._group_name)
        
    def start(self):
        if self.bridge is None or self.light_controller is None:
            print("Setting up a connection to the Hue Bridge")
            self.setup()
        self.process_monitor.block_until_process_detected()
        print("Backing up the lights"); self.light_controller.save_state()
        print("Getting initial state of VLC"); self._update_vlc_state()
        while True:
            self._block_until_state_change()
            self._logic_controller(self._vlc_state_previous, self._vlc_state_now)

    def _update_vlc_state(self):
        self._vlc_state_previous = self._vlc_state_now
        self._vlc_state_now = self.vlc_tracker.get_state()

    def _block_until_state_change(self, polling_rate=5):
        """
        Block until VLC state has changed.
        :param double polling_rate: Checking frequency per second
        :returns bool:
        """
        sleep_time = 1 / polling_rate
        comparison = self._vlc_state_now
        print("Waiting for VLC state to change")
        while self.vlc_tracker.get_state() == comparison:
            time.sleep(sleep_time)
        self._update_vlc_state()
        print("VLC has changed from '{0}' to '{1}'".format(comparison, self._vlc_state_now))
        return True
    
    def _logic_controller(self, before, after):
        if before == after:
            return
        # Make a backup each time we go from a stopped state to playing state
        if before == self.vlc_tracker.STATE_STOPPED and \
            after == self.vlc_tracker.STATE_PLAYING:
            self.light_controller.save_state()


        if after == self.vlc_tracker.STATE_PAUSED:
            # Low light ambience
            self.light_controller.ambient_lighting()
            print("Setting ambient lighting")
        elif after == self.vlc_tracker.STATE_PLAYING:
            # Turn off the lights
            self.light_controller.turn_off()
            print("Turning lights off")
        elif after == self.vlc_tracker.STATE_STOPPED:
            # Restore the lights
            self.light_controller.restore()
            print("Restoring lights")
        else:
            raise ValueError("Unhandled state value: " + after)

