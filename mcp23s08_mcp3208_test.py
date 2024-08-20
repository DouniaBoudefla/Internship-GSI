import spidev
import RPi.GPIO as GPIO
from time import sleep

REG_IODIR = 0x00  
REG_GPIO = 0x09

LED_PIN = 0

SPI_BUS_MCP23S08 = 0
SPI_CS_MCP23S08 = 0
CS_PIN_MCP23S08 = 8

SPI_BUS_MCP3208 = 0
SPI_CS_MCP3208 = 1

spi = spidev.SpiDev()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(CS_PIN_MCP23S08, GPIO.OUT)
GPIO.output(CS_PIN_MCP23S08, GPIO.HIGH)

def setup_mcp23s08():
    spi.open(SPI_BUS_MCP23S08, SPI_CS_MCP23S08)
    spi.max_speed_hz = 5000
    # Set all pins as inputs except pin 0
    write_register_mcp23s08(REG_IODIR, 0xFE)

def write_register_mcp23s08(register, value):
    GPIO.output(CS_PIN_MCP23S08, GPIO.LOW)
    spi.xfer([0x40, register, value])
    GPIO.output(CS_PIN_MCP23S08, GPIO.HIGH)

def read_register_mcp23s08(register):
    GPIO.output(CS_PIN_MCP23S08, GPIO.LOW)
    value = spi.xfer([0x41, register, 0x00])
    GPIO.output(CS_PIN_MCP23S08, GPIO.HIGH)
    return value[2]

def write_gpio_mcp23s08(value):
    write_register_mcp23s08(REG_GPIO, value)

def setup_mcp3208():
    spi.open(SPI_BUS_MCP3208, SPI_CS_MCP3208)
    spi.max_speed_hz = 5000

def read_adc_channel(channel):

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

    if value <= 0:
        value = 0
    elif value > 4095:
        value = 4095

    return value

def turn_on_led():
    write_gpio_mcp23s08(1 << LED_PIN)

def turn_off_led():
    write_gpio_mcp23s08(0 << LED_PIN)

def main():
    try:
        setup_mcp23s08()
        setup_mcp3208()
        
        while True:
            adc_value = read_adc_channel(0)
            print(f"ADC Channel 0 Value: {adc_value}")

            if adc_value > 2048:
                turn_on_led()
            else:
                turn_off_led()
            
            sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        spi.close()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
