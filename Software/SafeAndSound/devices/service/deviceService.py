from knotpy import *


def get_device_choices():
    credentials = {
	'uuid': '2414dbda-70f8-48cd-9718-4ab4be550000',
	'token': '51f16dee76bb838932ee298b933131ff02ebcf7d',
	'servername': 'localhost',
	'port': 3000
    }
    conn = KnotConnection('socketio', credentials)
    myThings = conn.getThings()
    my_list = [(things['uuid'],things['uuid']) for things in myThings]
    return my_list
