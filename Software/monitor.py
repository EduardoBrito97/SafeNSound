from knotpy import *
from credentials import *
from SafeAndSound import *
from time import gmtime, strftime
import sqlite3
import time

def had_changes(uuid, sensor_id, data = None):
	new_data =  conn.getData(uuid, limit=1)[0]['data']['value']
	return (data != new_data) and sensor_id == 69

def is_to_notify(isAlarmEnabled, bluetooth_enabled):
	return isAlarmEnabled or not bluetooth_enabled

def notify(device, user, wasopen):
	if wasopen:
		message = 'The device was opened on ' + strftime("%Y-%d-%m %H:%M:%S", gmtime()) + "."
		cursor.execute('''INSERT INTO notifications_notification(read, message, device_id, user_id)
                  VALUES(?,?,?,?)''', (False, message, device, user))
		db.commit()

conn = KnotConnection('socketio', credentials)
myThings = conn.getThings()
bluetooth_enabled = False

data = None
while True:
	db = sqlite3.connect('SafeAndSound/SafeAndSoundEngine.sqlite3')
	cursor = db.cursor()

	myThings = conn.getThings()
	time.sleep(0.3)
	for thing in myThings:
		uuid = thing['uuid']
		alldata = conn.getData(uuid, limit=1)
		sensor_id = alldata[0]['data']['sensor_id']
		if sensor_id == 96: 
			bluetooth_enabled = alldata[0]['data']['value']

		print(str(sensor_id) + "= " + str(conn.getData(uuid, limit=1)[0]['data']['value']) + " - " + strftime("%Y-%d-%m %H:%M:%S", gmtime()))
		print()
		if had_changes(uuid, sensor_id, data):
			data = alldata[0]['data']['value']
			device = cursor.execute('''SELECT id, userOwner_id, isAlarmEnabled FROM devices_device WHERE bluetooth_id=?''', (uuid,)).fetchone()
			alarm_enabled = False
			if device[2] == 1:
				alarm_enabled = True
			if is_to_notify(alarm_enabled, bluetooth_enabled):
				try:
					notify(device[0], device[1], not data)
				except:
					continue
	db.close()