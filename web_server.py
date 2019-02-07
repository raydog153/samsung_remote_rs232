import logging
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import base64
import re
import json
from remote_rs232 import RemoteRs232

PORT_NUMBER = 55000
KEY_MAPPINGS = dict(
    # KEY_POWER_STATUS=[0x00, 0x00, 0x00],
    KEY_POWEROFF=[0x00, 0x00, 0x98],
    KEY_POWERON=[0x00, 0x00, 0x99],
    KEY_POWER=[0x00, 0x00, 0x9D],
    KEY_MUTE='mute_toggle',
    KEY_SOURCE=[0x00, 0x00, 0x01],
    KEY_MENU=[0x00, 0x00, 0x1A],
    KEY_TOOLS=[0x00, 0x00, 0x4B],
    KEY_HDMI=[0x00, 0x00, 0x8B],
    KEY_SLEEP=[0x00, 0x00, 0x03],
    KEY_UP=[0x00, 0x00, 0x60],
    KEY_DOWN=[0x00, 0x00, 0x61],
    KEY_LEFT=[0x00, 0x00, 0x65],
    KEY_RIGHT=[0x00, 0x00, 0x62],
    KEY_CHUP='channel_up',
    KEY_CHDOWN='channel_down',
    KEY_PRECH='channel_previous',
    KEY_EXIT=[0x00, 0x00, 0x2d],
    KEY_VOLUP='volume_up',
    KEY_VOLDOWN='volume_down',
    KEY_ENTER=[0x00, 0x00, 0x68],
    KEY_RETURN=[0x00, 0x00, 0x58],
    KEY_INFO=[0x00, 0x00, 0x1f],
    KEY_PICTURE_SIZE=[0x00, 0x00, 0x3e]
)
KEYID_MAPPINGS = dict(
    # KEY_POWER_STATUS=[0x00, 0x00, 0x00],
    KEY_POWEROFF=[0x00, 0x00, 0x98],
    KEY_POWERON=[0x00, 0x00, 0x99],
    KEY_POWER=[0x00, 0x00, 0x9D],
    KEY_MUTE=[0x00, 0x00, 0x0f],
    KEY_SOURCE=[0x00, 0x00, 0x01],
    KEY_MENU=[0x00, 0x00, 0x1a],
    KEY_TOOLS=[0x00, 0x00, 0x4b],
    KEY_HDMI=[0x00, 0x00, 0x8b],
    KEY_SLEEP=[0x00, 0x00, 0x03],
    KEY_UP=[0x00, 0x00, 0x60],
    KEY_DOWN=[0x00, 0x00, 0x61],
    KEY_LEFT=[0x00, 0x00, 0x65],
    KEY_RIGHT=[0x00, 0x00, 0x62],
    KEY_CHUP=[0x00, 0x00, 0x12],
    KEY_CHDOWN=[0x00, 0x00, 0x10],
    KEY_PRECH=[0x00, 0x00, 0x13],
    KEY_EXIT=[0x00, 0x00, 0x2d],
    KEY_VOLUP=[0x00, 0x00, 0x07],
    KEY_VOLDOWN=[0x00, 0x00, 0x0b],
    KEY_ENTER=[0x00, 0x00, 0x68],
    KEY_RETURN=[0x00, 0x00, 0x58],
    KEY_INFO=[0x00, 0x00, 0x1f],
    KEY_PICTURE_SIZE=[0x00, 0x00, 0x3e]
)


def run_key_command(key_command):
    # Supported keys: PICTURE_SIZE, INFO, RETURN, ENTER,
    #   VOLDOWN, VOLUP, EXIT, PRECH, CHDOWN, CHUP, RIGHT, LEFT, DOWN, UP, SLEEP,
    #   HDMI, t=TOOLS, MENU, SOURCE, MUTE, POWEROFF, POWER_STATUS
    command_status = -1
    remote = RemoteRs232('/dev/ttyUSB0', log_level=logging.DEBUG)
    # key_command = base64.b64decode(key_command)
    print('Received command %s', key_command)

    power_is_on = remote.is_on()

    if key_command == 'KEY_POWER' or key_command == 'KEY_POWEROFF' or key_command == 'KEY_POWERON':
        remote.power_toggle()
        power_is_on = not power_is_on

    if power_is_on and KEY_MAPPINGS[key_command]:
        # Only run commands if TV is powered
        if isinstance(KEY_MAPPINGS[key_command], str):
            command_status = getattr(remote, KEY_MAPPINGS[key_command])()
        else:
            command_status = remote.send_key(key_command, KEY_MAPPINGS[key_command])

    remote.close()

    if power_is_on:
        print('sending tv is on')
    else:
        print('sending tv is off')
    return json.dumps({'power_status': power_is_on, 'command_status': command_status})


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        path_parts = self.path.split('/')
        response = '{}'
        key_command = ''
        print(path_parts)
        match = re.search('KEY_', path_parts[1])
        if path_parts[1] and match:
            key_command = path_parts[1]
            response = run_key_command(key_command)
            self.send_response(200)
        else:
            self.send_response(500)

        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # Send the html message
        self.wfile.write(response)
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
