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
	return isAlarmEnabled || bluetooth_enabled

def notify(device, user, wasopen):
	if wasopen:
		message = 'The device was opened on ' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "."
		cursor.execute('''INSERT INTO notifications_notification(read, message, device_id, user_id)
                  VALUES(?,?,?,?)''', (False, message, device, user))
		db.commit()


db = sqlite3.connect('SafeAndSound/SafeAndSoundEngine.sqlite3')
cursor = db.cursor()
conn = KnotConnection('socketio', credentials)
myThings = conn.getThings()

data = None
while True:
	myThings = conn.getThings()
	time.sleep(0.3)
	for thing in myThings:
		uuid = thing['uuid']
		alldata = conn.getData(uuid, limit=1)
		sensor_id = alldata[0]['data']['sensor_id']
		bluetooth_enabled = False
		if sensor_id == 96:
			bluetooth_enabled = alldata[0]['data']['value'] 
		if had_changes(uuid, sensor_id, data):
			data = alldata[0]['data']['value']
			device = cursor.execute('''SELECT id, userOwner_id, isAlarmEnabled FROM devices_device WHERE bluetooth_id=?''', (uuid,)).fetchone()		
			if is_to_notify(device[2]):
				try:
					notify(device[0], device[1], not data)
				except:
					continue