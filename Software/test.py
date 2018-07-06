from knotpy import *
from credentials import *
conn = KnotConnection('socketio', credentials)

myThings = conn.getThings()

for thing in myThings:
	data = conn.getData(thing['uuid'], limit=1)
	print (data[0])
	'''print('Set data')
	if thing.get('schema'):
		for sensor in thing.get('schema'):
			if sensor['name'] == 'LED':
				conn.setData(thing['uuid'], sensor['sensor_id'], True)
	print(60*'*')'''