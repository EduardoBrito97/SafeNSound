from knotpy import *
from credentials import *
from SafeAndSound import *


def had_changes(data = None):
	new_data =  conn.getData(thing['uuid'], limit=1)[0]['data']['value']
	return data != new_data

def is_to_notify(device = None):
	return True

def notify(device, user, wasopen):
	message = 'Device was closed.'
	if wasopen:
		message = 'Device was opened.'
	notification = notifications.models.Notification(user=user, device=device, read=False, message=message)
	Notification.save()

conn = KnotConnection('socketio', credentials)
myThings = conn.getThings()

data = None
while True:
	if had_changes(data[0]['data']['value']):
		open_sensor = conn.getData(thing['uuid'], limit=1)[0]['data']['value']
		if is_to_notify():
			try:
				device = device.models.Device.objects.get(bluetooth_id=open_sensor)
				user = device.user
				notify(device, user, not open_sensor)
			except:
				continue