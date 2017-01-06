from TSL2561 import TSL2561
import RPi.GPIO as GPIO
import time
import datetime
import asyncio
import smbus
import logging

def dif_millis(start_time):
	dt = datetime.datetime.now() - start_time
	ms = (dt.days * 24 * 60 * 60 +dt.seconds) + 1000 + dt.microseconds / 1000.00
	return int(ms)

@asyncio.coroutine
def detect_light():
	global __EXIT_FLAG
	while not __EXIT_FLAG :
		lux = tsl.get_lux()
		logging.debug("Lux = {}".format(lux))
		yield from asyncio.sleep(5 )

@asyncio.coroutine
def detect_sound():
	global __EXIT_FLAG
	last_detect = datetime.datetime.now()
	sound_detected = False
	while not __EXIT_FLAG :
		yield from asyncio.sleep(0.005) # debounce for 5mSec
		timestamp = time.time()
		stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

		if GPIO.input(__SOUND_PIN) == GPIO.LOW :
			last_detect = datetime.datetime.now()
			if not sound_detected :
				logging.debug('Sound is detected at {}'.format(stamp))
				sound_detected = True 
		else :
			if dif_millis(last_detect) > __SOUND_DETECTION_INT and sound_detected :
				sound_detected = False

@asyncio.coroutine
def detect_hall_effect():
	global __EXIT_FLAG
	last_detect = datetime.datetime.now()
	hall_detected = False
	while not __EXIT_FLAG :
		yield from asyncio.sleep(0.005) # debounce for 5mSec
		timestamp = time.time()
		stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
		if GPIO.input(__HALL_PIN) == GPIO.HIGH :	
			last_detect = datetime.datetime.now()
			if not hall_detected :
				logging.debug("Door is opened at {}".format(stamp))
				hall_detected = True
		else :
			if dif_millis(last_detect) > __HALL_DETECTION_INT  and hall_detected :
				hall_detected = False
				logging.debug("Door is closed at {}".format(stamp))

		
__SOUND_DETECTION_INT = 1000 # milliseconds
__HALL_DETECTION_INT = 1000 # milliseconds
__EXIT_FLAG = False
__HALL_PIN = 21 # GPIO 21 / PIN 40
__SOUND_PIN = 20 # GPIO 20 / PIN 38

GPIO.setmode(GPIO.BCM)

GPIO.setup(__HALL_PIN , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(__SOUND_PIN , GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
tsl =  TSL2561(addr=0x39,bus=smbus.SMBus(1),chan=1)
tsl._start()
logging.basicConfig(filename="log2.log",level=logging.DEBUG)

loop = asyncio.get_event_loop()
tasks = [
		asyncio.async(detect_light()),
		asyncio.async(detect_sound()),
		asyncio.async(detect_hall_effect())
	]

try :
	loop.run_until_complete(asyncio.gather(*tasks))

except KeyboardInterrupt :
	__EXIT_FLAG = True
finally :
	loop.close()
	GPIO.remove_event_detect([__SOUND_PIN,__HALL_PIN])
	GPIO.cleanup([__SOUND_PIN,__HALL_PIN])
	tsl._stop()
