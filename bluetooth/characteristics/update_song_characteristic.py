import json
from bluetooth.service import Characteristic

from bluetooth.descriptors.update_song_descriptor import UpdateSongDescriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

UPDATE_SONG_CHARACTERISTIC_UUID = "00000006-710e-4a5b-8d75-3e5b444bc3cf"

class UpdateSongCharacteristic(Characteristic):
    def __init__(self, service):
        self.notifying = False
        self.all_data = ''

        Characteristic.__init__(
                self, UPDATE_SONG_CHARACTERISTIC_UUID,
                ["write"], service)
        self.add_descriptor(UpdateSongDescriptor(self))

    def get_update_song(self):
        return None

    def set_update_song_callback(self):
        if self.notifying:
            value = self.get_update_song()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])

        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return

        self.notifying = True

        value = self.get_update_song()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_update_song_callback)

    def doesSongExist(self, song_data, key):
        for s_id, s_info in song_data.items():
            if (s_id == key):
                return True
        return False

    def WriteValue(self, value, options):
        str_value = '%s' % ''.join([str(v) for v in value])
        print("Recieved Update Song value: %s" % str_value)

        self.all_data = self.all_data + str_value

        if (str_value[-1] != '}'):
          return
        print("full message: %s" % self.all_data)

        updated_song = json.loads(self.all_data)
        self.all_data = ''
        f = open('./data/songs.json')
        existingSongData = json.load(f)
        f.close()

        if (self.doesSongExist(existingSongData, updated_song['id']) == False):
            raise Exception("Song doesn't exist")
        
        existingSongData[updated_song['id']] = { "name": updated_song['name'], "bpm": updated_song['bpm'], "file_name": existingSongData[updated_song['id']]['file_name']}
        f = open('./data/songs.json', 'w')
        f.write(json.dumps(existingSongData))
        f.close()
        print('Saved successfully')
        

    def StopNotify(self):
        self.notifying = False

    def ReadValue(self, options):
        value = self.get_update_song()

        return value