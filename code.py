from bm_serial import BristlemouthSerial
import board
import digitalio
import time
import adafruit_tsl2591
import ms5803
i2c = board.I2C()
sensorL = adafruit_tsl2591.TSL2591(i2c)


from adafruit_onewire.bus import OneWireBus
import adafruit_ds18x20
ow_bus = OneWireBus(board.D5)
devices = ow_bus.scan()
ds18b20 = adafruit_ds18x20.DS18X20(ow_bus, devices[0])
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
bm = BristlemouthSerial()
last_send = time.time()


Psensor = ms5803.MS5803(i2c, address=0x76)
pressure = Psensor.get_measurements(pressure_units="mbar")



while True:
    now = time.time()
    if now - last_send > 15:
        led.value = True
        last_send = now
        print("publishing", now)

        #bm.spotter_tx(b"sensor1: 1234.56, binary_ok_too: \x00\x01\x02\x03\xff\xfe\xfd")
        bm.spotter_log(
            "Temperature_test.log",
            "Sensor 1:"+'Temperature: {0:0.3f} °C'.format(ds18b20.temperature)+ 'Light: {0}lux'.format(sensorL.lux) + "Pressure: {:.2f} mbar".format(pressure)
        )
        led.value = False
