import logging
import socket
import base64
from remote_rs232 import RemoteRs232


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 55000  # initiate port no above 1024
    print("Will bind on: " + str(host) + ":" + str(port))

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    while True:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))

        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received then wait for next client
            conn.close()
            continue
        print("from connected client: " + str(data))
        parsed_data = str(data).split('samsung')
        if parsed_data[2]:
            command = base64.b64decode(parsed_data[2])
            print('Received command %s', command)
            remote = RemoteRs232('/dev/ttyUSB0', log_level=logging.DEBUG)

            if command == 'KEY_POWEROFF':
                remote.power_toggle()
            elif remote.is_on():
                # Only run commands if TV is powered
                print('TV is on, lets execute command!')
                 # TODO
                #remote.power_toggle()
            remote.close()
        else:
            print('Unable to parse command from data')

        # Send response back
        # First 3 bytes are TV name length
        # Next is name
        # Next is response length
        # Next is response itself
        data = b"\x00\x00\x0a"
        data += "Living Room"
        data = b"\x00\x04"
        data += b"\x64\x00\x01\x00"
        conn.send(data.encode())  # send data to the client
        conn.close()  # close the connection


if __name__ == '__main__':
    server_program()
