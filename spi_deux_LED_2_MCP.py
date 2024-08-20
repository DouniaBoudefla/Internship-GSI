import spidev
import RPi.GPIO as GPIO
from time import sleep 

spibus = spidev.SpiDev()
spibus.open(0,0)
spibus.open(0,1)
spibus.max_speed_hz = 5000

CS_PIN_0 = 8
CS_PIN_1 = 7

REG_IODIR = 0x00
REG_GPIO = 0x09

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CS_PIN_0, GPIO.OUT)
GPIO.setup(CS_PIN_1, GPIO.OUT)


def spi_write(cs, register, value):
    GPIO.output(cs, GPIO.LOW)
    spibus.xfer([0x40, register, value])
    GPIO.output(cs, GPIO.HIGH)


def spi_read(cs, register):
    GPIO.output(cs, GPIO.LOW)
    response = spibus.xfer([0x41, register, 0x00])
    GPIO.output(cs, GPIO.HIGH)
    return response[2]

def set_direction(cs, direction):
    spi_write(cs, REG_IODIR,direction)

def write_gpio(cs, value):
    spi_write(cs, REG_GPIO, value)

def read_gpio(cs):  
    return spi_read(cs, REG_GPIO)


set_direction(CS_PIN_0, 0xfe)
set_direction(CS_PIN_1, 0xfe)

try:
    while True:
        write_gpio(CS_PIN_0, 0x01)
        write_gpio(CS_PIN_1, 0x00)
        sleep(1)

        write_gpio(CS_PIN_0, 0x00)
        write_gpio(CS_PIN_1, 0x01)
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    spibus.close()
    GPIO.cleanup()
