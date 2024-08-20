import spidev
import RPi.GPIO as GPIO 
from time import sleep

spibus = spidev.SpiDev()
spibus.open(0,0)
spibus.max_speed_hz = 5000

def read_channel(spi, channel):
    (msg_up, msg_dn) = (
        (0x06, 0x00) if channel == 0
        else (0x06, 0x40) if channel == 1
        else (0x06, 0x80) if channel == 2
        else (0x06, 0xC0) if channel == 3
        else (0x07, 0x00) if channel == 4
        else (0x07, 0x40) if channel == 5
        else (0x07, 0x80) if channel == 6
        else (0x07, 0xC0)
    )

    resp = spi.xfer([msg_up, msg_dn, 0x00])
    value = (resp[1] << 8) + resp[2]
    value = int(value)

    '''
    if value <= 0:
        value = 0
    elif value > 4095:
        value = 4095
    '''
    return value

while True:
    value = read_channel(spibus,0)

    print("Value read for canal 0:")
    print(value) 
    sleep(1)

