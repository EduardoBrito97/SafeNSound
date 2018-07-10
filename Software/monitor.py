from knotpy import *
from credentials import *
from SafeAndSound import *
from time import gmtime, strftime
import sqlite3
import time
from datetime import datetime

def had_changes(uuid, sensor_id, data = None):
	#pegar data atual
	new_data =  conn.getData(uuid, limit=1)[0]['data']['value']
	#houve mudanças?
	return (data != new_data) and sensor_id == 69

def is_to_notify(isAlarmEnabled, bluetooth_enabled):
	return isAlarmEnabled or not bluetooth_enabled

def notify(device, user, wasopen):
	#inserir notificacao no banco caso tenha sido aberta, obs: com timestamp
	if wasopen:
		message = 'The device was opened on ' + strftime("%Y-%d-%m %H:%M:%S", time.localtime()) + "."
		cursor.execute('''INSERT INTO notifications_notification(read, message, device_id, user_id)
                  VALUES(?,?,?,?)''', (False, message, device, user))
		db.commit()

conn = KnotConnection('socketio', credentials)
myThings = conn.getThings()
bluetooth_enabled = False

data = None
while True:
	#apenas abrindo o banco
	db = sqlite3.connect('SafeAndSound/SafeAndSoundEngine.sqlite3')
	cursor = db.cursor()

	#pegando todos os things conectados a cada 0.3 seg
	myThings = conn.getThings()
	time.sleep(0.3)
	#pegando apenas os things que estão online e que possuem dados para ser retirados
	online_things = [(things) for things in myThings if ('online' in things and things['online'] == True and ('schema' in things))]
	for thing in online_things:
		uuid = thing['uuid']
		alldata = conn.getData(uuid, limit=1)
		#pega o sensor do thing; 69 = abertura e 96 = bluetooth
		sensor_id = alldata[0]['data']['sensor_id']
		if sensor_id == 96: 
			bluetooth_enabled = alldata[0]['data']['value']

		if had_changes(uuid, sensor_id, data):
			#printando log quando acontece mudança
			print(str(sensor_id) + " = " + str(conn.getData(uuid, limit=1)[0]['data']['value']) + " - " + strftime("%Y-%d-%m %H:%M:%S", time.localtime()))
	
			data = alldata[0]['data']['value']
			#pegando os dados do device pra poder criar a notificacao e ver se a notificacao vai ser criada ou não
			device = cursor.execute('''SELECT id, userOwner_id, isAlarmEnabled FROM devices_device WHERE bluetooth_id=?''', (uuid,)).fetchone()
			alarm_enabled = False
			if device[2] == 1:
				alarm_enabled = True
			if is_to_notify(alarm_enabled, bluetooth_enabled):
				try:
					notify(device[0], device[1], not data)
				except:
					continue
	#fechando o banco pra não sobrecarregar de consulta
	db.close()
