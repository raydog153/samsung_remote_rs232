import logging
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import base64
import re
from remote_rs232 import RemoteRs232

PORT_NUMBER = 55000
KEY_MAPPINGS = dict(
    # KEY_POWER_STATUS=[0x00, 0x00, 0x00],
    KEY_POWEROFF=[0x00, 0x00, 0x98],
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
    remote = RemoteRs232('/dev/ttyUSB0', log_level=logging.DEBUG)
    # key_command = base64.b64decode(key_command)
    print('Received command %s', key_command)

    power_is_on = remote.is_on()

    if key_command == 'KEY_POWER' or key_command == 'KEY_POWEROFF' or key_command == 'KEY_POWERON':
        remote.power_toggle()
        power_is_on = not power_is_on

    if power_is_on and KEY_MAPPINGS[key_command]:
        # Only run commands if TV is powered
        remote.send_key(key_command)

    remote.close()
    if power_is_on:
        print('sending tv is on')
        return True
    else:
        print('sending tv is off')
        return False


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        path_parts = self.path.split('/')
        response = ''
        key_command = ''
        print(path_parts)
        match = re.search('KEY_', path_parts[1])
        if path_parts[1] and match:
            key_command = path_parts[1]
            response = run_key_command(key_command)
            self.send_response(200)
        else:
            self.send_response(500)

        self.send_header('Content-type', 'text/json')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World: " + key_command + str(response))
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
