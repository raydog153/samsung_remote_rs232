#!/usr/bin/env python

import logging
from remote_rs232 import RemoteRs232


def main():
    # TODO argparse
    # Add console arg parsing so we can pass in serial port
    # /dev/tty.usbserial-FTE2V28X

    # BAUD must be 9600 for sending commands
    remote = RemoteRs232('/dev/ttyUSB0', log_level=logging.DEBUG)

    #remote.power_toggle()
    remote.get_status_power()

    #remote.volume_set(8)
    #remote.volume_up()
    #remote.key_volup()

    #remote.set_source('hdmi2')

    #remote.key_factory()
    #remote.key_3speed()
    #remote.key_dnet()
    remote.close()


if __name__ == '__main__':

    main()
