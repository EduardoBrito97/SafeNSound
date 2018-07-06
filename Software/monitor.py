from knotpy import *
from credentials import *
from SafeAndSound import *
import sqlite3
import time

def had_changes(uuid, sensor_id, data = None):
	new_data =  conn.getData(uuid, limit=1)[0]['data']['value']
	return (data != new_data) and sensor_id == 69

def is_to_notify(device = None):
	return True

def notify(device, user, wasopen):
	message = 'Device was closed.'
	if wasopen:
		message = 'Device was opened.'
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
		if had_changes(uuid, sensor_id, data):
			data = alldata[0]['data']['value']
			if is_to_notify():
				try:
					device = cursor.execute('''SELECT id, userOwner_id FROM devices_device WHERE bluetooth_id=?''', (uuid,)).fetchone()
					notify(device[0], device[1], not data)
				except:
					continue