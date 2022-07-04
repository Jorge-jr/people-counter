import datetime
import requests
import json


blacklist = ["00:e0:4c:36:1f:16", "00:e0:4c:53:44:58", "33:33:00:00:00:16", "5c:cd:5b:08:56:0b",
             "68:02:b8:52:bd:b3", "6a:02:b8:52:48:85", "86:33:2e:ab:7a:4b", "b8:27:eb:07:86:33",
             "b8:27:eb:62:f5:18", "b8:27:eb:77:d2:5f", "bc:8c:cd:67:05:e1", "bd:7f:c1:9f:00:00",
             "bd:7f:c1:9f:04:00", "bd:7f:c1:9f:d6:00", "c0:38:96:a1:bd:7f", "C8:5D:38:1C:6A:A9",
             "ff:ff:ff:ff:ff:ff"]


class Device(object):

    def __init__(self, address, number_of_sniffers, sniffer_index, is_in, rssi):
        self.address = address
        self.rssi = [-100] * number_of_sniffers
        self.rssi[sniffer_index] = int(rssi)
        self.last_seen = datetime.datetime.now()
        self.count = 1
        self.blacklisted = address in blacklist
        try:
            # print("https://api.macvendors.com/{}".format(self.address))
            # self.vendor = requests.get("https://api.macvendors.com/{}".format(self.address)).content.decode('ascii')
            self.vendor = json.loads(requests.get(
                "http://www.macvendorlookup.com/api/v2/{}".format(self.address)).content.decode('ascii'))[0]['company']
            print(self.vendor)
        except Exception as error:
            print(error)
            self.vendor = "vendor not found"
        #finally:
            #if self.vendor in vendor_blacklist:
                #self.blacklisted = True

        if is_in:
            self.last_seen_in = datetime.datetime.now()
        else:
            self.last_seen_in = datetime.datetime.now() - datetime.timedelta(seconds=31)

    def sight(self, is_in, sniffer_index, rssi):
        self.last_seen = datetime.datetime.now()
        if is_in:
            self.last_seen_in = datetime.datetime.now()
        self.rssi[sniffer_index] = int(rssi)
        self.count += 1

    def get_address(self):
        return self.address

    def check_in(self, in_sniffer_indexes: list):
        timer = datetime.timedelta(seconds=60)
        if (datetime.datetime.now() - self.last_seen_in) >= timer or self.blacklisted:
            return False
        for index in in_sniffer_indexes:
            try:
                if self.rssi[index] >= max(self.rssi):
                    return True
            except Exception as e:
                print(index, in_sniffer_indexes, e, self.rssi)
        return False
