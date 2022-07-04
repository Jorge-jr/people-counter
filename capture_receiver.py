from device import Device
from sniffer import Sniffer
import datetime


class Receiver(object):

    def __init__(self, sniffers):
        self.devices = []
        self.sniffers = [Sniffer(snf) for snf in sniffers]

    def receive_capture(self, address, snf, rssi):
        sniffer, sniffer_index = self.get_sniffer(snf)
        with open('captures.txt', 'a') as file:
            if address == '00:16:98:1c:20:75' or address == '00:16:98:1b:fa:17':
                file.write(str(datetime.datetime.now()) + ' ' + address + ' ' + snf + ' ' + rssi + ' \n')
        for dev in self.devices:
            if dev.get_address() == address:
                dev.sight(sniffer.is_in, sniffer_index, rssi)
                sniffer.insert_device(dev)
                return True
        self.devices += [Device(address, len(self.sniffers), sniffer_index, sniffer.is_in, rssi)]
        print("new address: ", address)
        return False

    def get_sniffer(self, snf):
        index = 0
        for sniffer in self.sniffers:
            if sniffer.name == snf:
                return sniffer, index
            index += 1

    def get_in_sniffers_indexes(self):
        return [self.sniffers.index(sniffer) for sniffer in self.sniffers if sniffer.is_in]

    def snapshot(self):
        in_devices = [device for device in self.devices if device.check_in(self.get_in_sniffers_indexes())]
        with open("snaps.txt", 'a') as snaps:
            snaps.write(
                'Time: ' + datetime.datetime.now().strftime('%H:%M:%S') + ' - count: ' + str(len(in_devices)) + "\n")
            for dev in in_devices:
                snaps.write(dev.address + '\n')
