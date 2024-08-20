import spidev
import RPi.GPIO as GPIO
from time import sleep

spibus = spidev.SpiDev()
spibus.open(0,0)
spibus.max_speed_hz = 5000

CS_PIN = 8

REG_IODIR = 0x00
REG_GPIO = 0x09

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CS_PIN,GPIO.OUT)

def spi_write(register, value):
    GPIO.output(CS_PIN, GPIO.LOW)
    spibus.xfer([0x40,register,value])
    GPIO.output(CS_PIN, GPIO.HIGH)

def spi_read(register):
    GPIO.output(CS_PIN, GPIO.LOW)
    response = spibus.xfer([0x41,register,0x00])
    GPIO.output(CS_PIN,GPIO.HIGH)
    return response[2]

def set_direction(direction):
    spi_write(REG_IODIR,direction)

def write_gpio(value):
    spi_write(REG_GPIO, value)

def read_gpio():
    return spi_read(REG_GPIO)

set_direction(0xfe)

try:
    while True:
        button_state = read_gpio() & 0x01
        if button_state == 1:
            write_gpio(0x01)
            print("Bouton pressed, LED turned ON")
        else:
            write_gpio(0x00)
            print("Button released, LED turned OFF")
        sleep(1)
except KeyboardInterrupt:
    pass
finally:
    spibus.close()
    GPIO.cleanup()