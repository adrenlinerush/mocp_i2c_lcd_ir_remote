from evdev import *
import subprocess

devices = [InputDevice(path) for path in list_devices()]
irin = None
for device in devices:
    if(device.name=="meson-ir"):
        irin = device

if(irin == None):
    print("Unable to find IR input device, exiting")
    exit(1)

def readInputEvent(device):
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            data = categorize(event)
            if data.keystate==data.key_down:
              reponse = data.keycode
              match (data.keycode):
                case "KEY_PLAYPAUSE":
                  response = subprocess.check_output(['mocp', '-G']) 
                case "KEY_BACK":
                  response = subprocess.check_output(['mocp', '-r']) 
                case "KEY_FORWARD":
                  response = subprocess.check_output(['mocp', '-f']) 
                case "KEY_VOLUMEUP":
                  response = subprocess.check_output(['mocp', '--volume=+5']) 
                case "KEY_VOLUMEDOWN":
                  response = subprocess.check_output(['mocp', '--volume=-5']) 
                case "KEY_SHUFFLE":
                  response = subprocess.check_output(['mocp', '--toggle=shuffle']) 

while True:
    readInputEvent(irin)
