# -*- coding: utf-8 -*-
import threading
import microgear.client as netpie
from ScratchPy import *
# ---------------------------------------------
_key = '[Your NETPIE KEY]'
_secret = '[Your NETPIE SECRET]'
_app = '[Your NETPIE APPLICATION NAME]'

_gear_name = '[Your Alias Name]' 
_other_gear_names = ['[Your Opposit Alias Name]']
_stop_flag = False
_topic = '/pong_game'

#-- Event Handler
def on_disconnect():
	pass
			
def on_connect():
	print('Connected ')
	#netpie.subscribe(_topic)
	pass
	
def on_message(topic, msg):
	global psc, _stop_flag, mos_client, _ips, y_pos, _dir,_topic
	
	msg = msg.replace("b'",'').replace("'",'')
	data = ''
	if msg == 'new start' :
		psc.sensorupdate({'game_state','ready'})
	elif msg == 'opposit lose':
		psc.broadcast('opposit lose')
	else :
		data = msg.split(":")
	
	if len(data) &gt; 0 and data[0] == 'ball':
		_ypos = data[1]
		_dir = data[2]
		if _stop_flag == True:
			send_to_opposit("ball:"+str(y_pos)+":"+str(_dir))
		else :
			# -- forward message to Scrath 
			psc.sensorupdate({"y_pos":_ypos})
			psc.sensorupdate({"dir":_dir})	
			psc.broadcast('activate')

def on_present(gearkey):
	#print("{0} is online".format(gearkey))
	pass
	
def on_absent(gearkey):
	#print("{} is out".format(gearkey))
	pass
	
def on_error(msg):
	pass
		
		
def parse_data(data):
	tmp = ['you_lose','send_pong_data','let_move','game_state','new_start']
	global _dir,y_pos, _stop_flag	

	if data[0] == 'broadcast' :
		if data[1] == 'quit':
			_stop_flag = True
			return -1
		elif data[1] == 'sendout':	
			return 1
		elif data[1] == 'new_start':
			send_to_opposit('new start')
			return 0
		elif data[1] == 'i_lose':
			send_to_opposit('opposit lose')
			return 0
		elif not data[1] in tmp : # filter out unused broadcasting			
			if data[2] is None :			
				temp = data[1].split(':')
				k = temp[0]
				v = temp[1]
			else :
				k = data[1].replace(':','')
				v = data[2]
			if k == 'direction' :	 
				_dir = v
			elif k == 'ypos':
				y_pos = v
			return 0	

def send_to_opposit(data):
	target = random.choice(_other_gear_names)	
	netpie.chat(target,data)
	

def run():
	global psc,_ips,_dir,y_pos, _stop_flag
	_dir = y_pos = 0
	psc = Py2Scratch14()
	psc.connect()	
	
	netpie.create(_key,_secret,_app)
	netpie.on_connect = on_connect
	netpie.on_message = on_message
	netpie.on_present = on_present
	netpie.on_absent = on_absent
	netpie.setalias(_gear_name)
	netpie.connect(False)
	
	while True :
		res = parse_data(psc.receive())
		if res == 1  and _stop_flag == False:
			send_to_opposit("ball:"+str(y_pos)+":"+str(_dir))
						
	psc.end()	
# ---------------------------------------------

if __name__ == "__main__":
	t = threading.Thread(target=run)
	t.start()
	
