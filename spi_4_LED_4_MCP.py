import spidev
import RPi.GPIO as GPIO
from time import sleep

spibus_0 = spidev.SpiDev()
spibus_1 = spidev.SpiDev()

spibus_0.open(0,0)
spibus_0.open(0,1)
spibus_1.open(1,0)
spibus_1.open(1,1)

spibus_0.max_speed_hz = 5000
spibus_1.max_speed_hz = 5000

CS_PIN_0_0 = 8
CS_PIN_0_1 = 7
CS_PIN_1_0 = 12
CS_PIN_1_1 = 11

REG_IODIR = 0x00
REG_GPIO = 0x09

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CS_PIN_0_0, GPIO.OUT)
GPIO.setup(CS_PIN_0_1, GPIO.OUT)
GPIO.setup(CS_PIN_1_0, GPIO.OUT)
GPIO.setup(CS_PIN_1_1, GPIO.OUT)


def spi_write(bus, cs, register, value):
    GPIO.output(cs, GPIO.LOW)
    if bus == 0:
        spibus_0.xfer([0x40, register, value])
    else:
        spibus_1.xfer([0x40, register, value])
    GPIO.output(cs, GPIO.HIGH)

def spi_read(bus, cs, register):
    GPIO.output(cs, GPIO.LOW)
    if bus == 0:
        response = spibus_0.xfer([0x41, register, 0x00])
    else: 
        response = spibus_1.xfer([0x41, register, 0x00])
    GPIO.output(cs, GPIO.HIGH)
    return response[2]

def set_direction(bus, cs, direction):
    spi_write(bus, cs, REG_IODIR,direction)

def write_gpio(bus, cs, value):
    spi_write(bus, cs, REG_GPIO, value)

def read_gpio(bus, cs):  
    return spi_read(bus, cs, REG_GPIO)

set_direction(0,CS_PIN_0_0,0xfe)
set_direction(0,CS_PIN_0_1,0xfe)
set_direction(1,CS_PIN_1_0,0xfe)
set_direction(1,CS_PIN_1_1,0xfe)

try:
    while True: 
        write_gpio(0,CS_PIN_0_0,0x01)
        write_gpio(0,CS_PIN_0_1,0x00)
        write_gpio(1,CS_PIN_1_0,0x00)
        write_gpio(1,CS_PIN_1_1,0x00)

        sleep(1)

        write_gpio(0,CS_PIN_0_0,0x00)
        write_gpio(0,CS_PIN_0_1,0x01)
        write_gpio(1,CS_PIN_1_0,0x00)
        write_gpio(1,CS_PIN_1_1,0x00)

        sleep(1)

        write_gpio(0,CS_PIN_0_0,0x00)
        write_gpio(0,CS_PIN_0_1,0x00)
        write_gpio(1,CS_PIN_1_0,0x01)
        write_gpio(1,CS_PIN_1_1,0x00)

        sleep(1)

        write_gpio(0,CS_PIN_0_0,0x00)
        write_gpio(0,CS_PIN_0_1,0x00)
        write_gpio(1,CS_PIN_1_0,0x00)
        write_gpio(1,CS_PIN_1_1,0x01)

except KeyboardInterrupt:
    pass

finally:
    spibus_0.close()
    spibus_1.close()
    GPIO.cleanup()