# Samsung RS232 Remote Control
Script to control Samsung Products via RS232

## Products supported:
Samsung TV's

## Supported/Tested models
- LN52A750
- UN40H5203

## Current features
- Power on/off/toggle
- Send Remote Key commands
- Send Status commands

## Future features
- Support RS233 to Ethernet devices
- Support REST API
- Serial debug output mode

## Python versions supported
- TBD

## Installation instructions
- Requirements
  - Python module serial: pip install pyserial (If you install wrong serial module by mistake you can undo using: pip uninstall serial)

## Running web server
sudo nohup python /path/samsung_remote_rs232/web_server.py > output.log &
