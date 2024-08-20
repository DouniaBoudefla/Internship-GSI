import spidev
import RPi.GPIO as GPIO
from time import sleep

spibus = spidev.SpiDev()
spibus.open(0,1)
spibus.mode = 0b01
spibus.max_speed_hz = 5000

CS_PIN = 7

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CS_PIN,GPIO.OUT)

def spi_test():
    GPIO.output(CS_PIN,GPIO.LOW)
    response = spibus.xfer([0x50, 0x0, 0xf1])
    sleep(2)
    GPIO.output(CS_PIN,GPIO.HIGH)
    print(response)

while True:
    spi_test()
    sleep(2)