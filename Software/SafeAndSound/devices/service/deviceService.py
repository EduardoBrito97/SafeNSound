from knotpy import *


def get_device_choices():
    try:
        credentials = {
        'uuid': '4cea630a-172f-4188-aef3-b4144ed80000',
        'token': 'b4943ddfd9ac00beef5c388501ea265b99876e1b',
        'servername': 'localhost',
        'port': 3000
        }
        conn = KnotConnection('socketio', credentials)
        myThings = conn.getThings()
        my_list = [(things['uuid'], things['name']) for things in myThings if ('online' in things and things['online'] == True and ('schema' in things))]
        print('')
        return my_list
    except:
        print('crashed on devices service')
        return tuple(())
