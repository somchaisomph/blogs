import smbus
import time
import asyncio
# Reference : https://cdn-shop.adafruit.com/datasheets/TSL2561.pdf
class TSL2561():
	def __init__(self,addr=0x39,bus=None,chan=1):
		self.addr = addr	
		if not bus :
			self.bus = smbus.SMBUS(chan)
		else :
			self.bus = bus
			
	def _start(self):
		# command = i2cset -y 1 tlsr_addr 0x80 0x03
		self.bus.write_byte_data(self.addr,0x80,0x03)
		
	def _stop(self):
		# command = i2cset -y 1 tlsr_addr 0x80 0x00
		self.bus.write_byte_data(self.addr,0x80,0x00)
		
	def _set_sampling_rate_worst(self,state='best'):
		if state == 'worst':
			# command = i2cset -y 1 tlsr_addr 0x81 0x00
			self.bus.write_byte_data(self.addr,0x81,0x00)
		elif state == 'medium':
			# command = i2cset -y 1 tlsr_addr 0x81 0x01
			self.bus.write_byte_data(self.addr,0x81,0x01)
		elif state == 'best':
			# command = i2cset -y 1 tlsr_addr 0x81 0x02
			self.bus.write_byte_data(self.addr,0x81,0x02)
		
	def get_ambiente(self):
		ambient_low_byte = self.bus.read_byte_data(self.addr,0x8c)
		ambient_high_byte = self.bus.read_byte_data(self.addr,0x8d)
		ambiente = ambient_high_byte*256 + ambient_low_byte
		return ambiente 
		
	def get_ir(self):
		ir_low_byte = self.bus.read_byte_data(self.addr,0x8e)
		ir_high_byte = self.bus.read_byte_data(self.addr,0x8f)
		ir = (ir_high_byte * 256) + ir_low_byte
		return ir
		
	def get_lux(self):
		ir = self.get_ir()
		amb = self.get_ambiente()
		if amb == 0 :
			return 0
		ratio = ir / float(amb)
		lux = 0 
		if 0 < ratio <= 0.50 :
			lux = (0.0304 * amb) - (0.062 * amb * (ratio**1.4))
		elif 0.50 < ratio <= 0.61:
			lux = (0.0224 * amb) - (0.031 * ir)
		elif 0.61 < ratio <= 0.80:
			lux = (0.0128 * amb) - (0.0153 * ir)
		elif 0.80 < ratio <= 1.3 :
			lux = (0.00146 * amb) - (0.00112 * ir)
		else :
			lux = 0
		return lux

@asyncio.coroutine
def detect_light():
	
if __name__ == "__main__":

	tsl =  TSL2561(addr=0x39,bus=smbus.SMBus(1),chan=1)
	tsl._start()
	try :
			while True :
		    lux = tlsr.get_lux()
		    print("Lux = {}".format(lux))
		    time.sleep(1)

	finally:
		tsl._stop()
