import binascii
import serial
import logging
import time


class RemoteRs232(object):
    """Class summary here

    More class info
    More class info

    Attributes:
        port_name: A string name of serial port to use for communicating with 
            the TV.  Example: '/dev/tty.usbserial-FTE2V28X'
        baud_rate: An integer specifying the baud rate of the serial port.
            Defaults to 9600, the setting for the Samsung LN52A750.
            9600, 19200, ....
        logger: A standard Python logging class instance.
    """

    CHANNEL_TYPE_ANALOG = 0x00
    CHANNEL_TYPE_DIGITAL = 0x80
    HEADER_BYTE1 = 0x08
    HEADER_BYTE2 = 0x22

    def __init__(self, port_name, log_level=logging.INFO, baud_rate=9600):
        """Initializes RemoteRs232 with the given settings.
        """
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.logger = logging.getLogger(__name__)
        self.init_logging(log_level)
        self.port = self.open()

    # Power Commands - CMD1=0x00
    def power_toggle(self):
        """
        received cb 14 13 47 e6 0e cb 3c 7c
        received cb 16 19 47 e6 0e c9 5c fc
        received 19 12 1b 47 e6 0e cb 58 5c
        """
        self.logger.info('toggling power')
        self.send_command('power', 0x00, 0x00, 0x00)

    def power_off(self):
        self.logger.info('power off')
        self.send_command('power', 0x00, 0x00, 0x01)

    def power_on(self):
        self.logger.info('power on')
        self.send_command('power', 0x00, 0x00, 0x02)

    # Volume Commands - CMD1=0x01
    def volume_set(self, volume_level):
        if volume_level > 100:
            self.logger.error('volume requested out of range: %d', volume_level)
            return

        self.logger.info('setting volume to %d', volume_level)
        self.send_command('volume', 0x00, 0x00, volume_level)

    def volume_up(self):
        self.logger.info('volume up')
        self.send_command('volume', 0x00, 0x01, 0x00)

    def volume_down(self):
        self.logger.info('volume down')
        self.send_command('volume', 0x00, 0x02, 0x00)

    # Mute Commands - CMD1=0x02
    def mute_toggle(self):
        self.logger.info('mute toggle')
        self.send_command('mute', 0x00, 0x00, 0x00)

    # Channel Analog Commands - CMD1=0x03
    def channel_up(self):
        self.logger.info('channel up')
        self.send_command('channel', 0x00, 0x01, 0x00)

    def channel_down(self):
        self.logger.info('channel down')
        self.send_command('channel', 0x00, 0x02, 0x00)

    def channel_previous(self):
        self.logger.info('channel ')
        self.send_command('channel', 0x00, 0x00, 0x00)

    # Channel Digital Commands - CMD1=0x04
    def channel_set(self, channel, channel_type=CHANNEL_TYPE_ANALOG):
        """
        # Digital channel format:
        #   channel = 4-1
        """
        # TODO
        if channel_type == RemoteRs232.CHANNEL_TYPE_ANALOG:
            self.logger.info('channel set to %s', channel)
            self.send_command('channel', channel_type, 0x00, channel)
        else:
            self.logger.info('digital channel set to %s', channel)
            channel_main = channel.split('-')[0]
            channel_sub = channel.split('-')[1]
            self.send_command('channel_digital', channel_type, channel_main, channel_sub)

    # Input Commands - CMD1=0x0a
    def set_source(self, source_name):
        self.logger.info('setting source to %s', source_name)
        number = 0
        if source_name is 'tv':
            source = 0
        elif source_name is 'av1':
            source = 1
        elif source_name is 'av2':
            source = 1
            number = 1
        elif source_name is 'av3':
            source = 1
            number = 2
        elif source_name is 'svideo1':
            source = 2
        elif source_name is 'svideo2':
            source = 2
            number = 1
        elif source_name is 'svideo3':
            source = 2
            number = 2
        elif source_name is 'comp1':
            source = 3
        elif source_name is 'comp2':
            source = 3
            number = 1
        elif source_name is 'comp3':
            source = 3
            number = 2
        elif source_name is 'pc':  # Also VGA
            source = 4
        elif source_name is 'hdmi1':
            source = 5
        elif source_name is 'hdmi2':
            source = 5
            number = 1
        elif source_name is 'hdmi3':
            source = 5
            number = 2
        elif source_name is 'hdmi4':
            source = 5
            number = 3
        elif source_name is 'dvi1':
            source = 6
        elif source_name is 'dvi2':
            source = 6
            number = 1
        elif source_name is 'dvi3':
            source = 6
            number = 2
        else:
            self.logger.error('invalid source name %s', source_name)
            return

        self.send_command('input', 0x00, source, number)

    # Picture Commands - CMD1=0x0b

    # Sound Commands - CMD1=0x0c
    def speaker_on(self):
        self.logger.info('speaker on')
        self.send_command('sound', 0x06, 0x00, 0x00)

    def speaker_off(self):
        self.logger.info('speaker off')
        self.send_command('sound', 0x06, 0x00, 0x01)

    # Key Commands - CMD1=0x0d
    def set_app(self, app_name):
        self.logger.info('setting app to %s', app_name)
        if app_name is 'smart_hub':
            app = 0x8c
        elif app_name is 'netflix':
            app = 0xf3
        elif app_name is 'amazon':
            app = 0xf4
        else:
            self.logger.error('invalid app name %s', app_name)
            return
        self.send_command('key', 0x00, 0x00, app)

    def key_factory(self):
        self.logger.info('key: !!!factory!!!')
        self.send_command('key', 0x00, 0x00, 0x3b)

    def key_3speed(self):
        self.logger.info('key: !!!3speed!!!')
        self.send_command('key', 0x00, 0x00, 0x3c)

    def key_volup(self):
        """
        08 22 0d 00 00 07 C2
        """
        self.logger.info('key: volume up')
        self.send_command('key', 0x00, 0x00, 0x07)

    def key_dnet(self):
        self.logger.info('key: !!!dnet!!!')
        self.send_command('key', 0x00, 0x00, 0xb7)

    def send_key(self, key_name):
        key_id = 0x00 # key_lookup(key_name)
        self.logger.info('key: %s (%s)', key_name, key_id)
        self.send_command('key', 0x00, 0x00, key_id)

    # Template for new methods
    def key_template(self):
        self.logger.info('key <key>')
        self.send_command('key', 0x00, 0x00, 0x00)

    # OSD/Setup Commands - CMD1=0x0e
    # ????

    # Status Commands - CMD1=0xf0
    def get_status_power(self):
        self.logger.info('request power status...')
        return self.send_command('status', 0x00, 0x00, 0x00)

    # Status Commands - CMD1=0xf0
    def get_status_volume(self):
        self.logger.info('request volume status...')
        self.send_command('status', 0x01, 0x00, 0x00)

    def is_on(self):
        # Function get_status_power doesn't actually work for status at all.
        # Returns success if TV is on, failure if TV is off
        # Hence hack to find out if TV is on or not...
        if self.get_status_power():
            return True
        else:
            return False

    def open(self):
        self.logger.debug('opening port %s', self.port_name)
        return serial.Serial(self.port_name, self.baud_rate, 8, serial.PARITY_NONE, serial.STOPBITS_ONE, xonxoff=0, rtscts=0, timeout=2)

    def close(self):
        self.logger.debug('closing %s', self.port_name)
        self.port.close()
        self.port = None

    def send_command(self, cmd_control_type, cmd2, cmd3, value):
        if cmd_control_type is 'power':
            # Power Commands - CMD1=0x00
            cmd1 = 0x00
        elif cmd_control_type is 'volume':
            # Volume Commands - CMD1=0x01
            cmd1 = 0x01
        elif cmd_control_type is 'mute':
            # Mute Commands - CMD1=0x02
            cmd1 = 0x02
        elif cmd_control_type is 'channel':
            # Channel Analog Commands - CMD1=0x03
            cmd1 = 0x03
        elif cmd_control_type is 'channel_digital':
            # Channel Digital Commands - CMD1=0x04
            cmd1 = 0x04
        elif cmd_control_type is 'input':
            # Input /SourceCommands - CMD1=0x0a
            cmd1 = 0x0a
        elif cmd_control_type is 'picture':
            # Picture Commands - CMD1=0x0b
            cmd1 = 0x0b
        elif cmd_control_type is 'sound':
            # Sound Commands - CMD1=0x0c
            cmd1 = 0x0c
        elif cmd_control_type is 'key':
            # Key Commands - CMD1=0x0d
            cmd1 = 0x0d
        elif cmd_control_type is 'osd':
            # OSD/Setup Commands - CMD1=0x0e
            cmd1 = 0x0e
        elif cmd_control_type is 'status':
            # Status Commands - CMD1=0xf0
            cmd1 = 0xf0
        else:
            self.logger.error('invalid control type name %s', cmd_control_type)
            return

        return self.send_command_raw(cmd1, cmd2, cmd3, value)

    def send_command_raw(self, cmd1, cmd2, cmd3, value):
        if not self.port.isOpen():
            self.logger.error('Tried to send a command but port was not open')
            return

        command = bytearray([RemoteRs232.HEADER_BYTE1, RemoteRs232.HEADER_BYTE2, cmd1, cmd2, cmd3, value])
        # TODO: Use seperate method for checksum, first validate
        # RemoteRs232.generate_checksum(command)
        checksum = -(sum(command) % 256) & 0xff
        command.append(checksum)

        hexstr = str(binascii.hexlify(command))
        formatted_hex = ' '.join(hexstr[i:i+2] for i in range(0, len(hexstr), 2))

        self.port.write(command)        
        self.logger.debug('sent %s', hexstr)
        self.logger.debug('sent %s', formatted_hex)

        resp = self.port.readline()
        formatted_resp = ' '.join("{:02x}".format(ord(c)) for c in resp)
        self.logger.debug('received %s', formatted_resp)

        resp2 = self.port.readline()
        formatted_resp2 = ' '.join("{:02x}".format(ord(c)) for c in resp2)
        self.logger.debug('received resp2 %s', formatted_resp2)

        if resp == b'\x03\x0c\xf1':
            self.logger.info('command response valid 3byte')
            return True
        elif resp == b'\x03\x0c\xf1\x00':
            self.logger.info('command response valid 4byte')
            return True
        elif resp == b'\x03\x0c\xff':
            #
            self.logger.info('command response failed')
            return False
        else:
            self.logger.error('command response unknown/failed')
            return False


    @staticmethod
    def generate_checksum(data):
        # Definition? 100 - (Sum of first 6 bytes)
        # Checksum (the 2's complement of the sum of all the values except for the CS value.)
        #data = value.decode("hex")
        byte_sum = 0
        for byte in data:
            byte_sum += byte
        print("Two's complement: %s", hex((~byte_sum + 1) & 0xFF))
        data = hex((~byte_sum + 1) & 0xFF)
        data = str(data)[2:]
        if len(data) < 2:
            data = '0' + data
        print("checksum " + data)
        return data

    def init_logging(self, log_level):
        """Initialize logging for the remote

        Args:
            log_level: A enum which can be DEBUG, INFO, WARNING, ERROR,
                or CRITICAL. Example: logging.INFO
        """
        self.logger.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
        stream_handle = logging.StreamHandler()
        stream_handle.setLevel(log_level)
        stream_handle.setFormatter(formatter)
        self.logger.addHandler(stream_handle)
        self.logger.debug('logging initialized')
