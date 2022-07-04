class Sniffer(object):

    def __init__(self, name):
        self.name = name
        self.is_in = False
        self.captured_devices = []

    def set_in_out(self):
        self.is_in = not self.is_in
        print("setting {} as in room device: {}".format(self.name, self.is_in))

    def insert_device(self, device):
        if device not in self.captured_devices:
            self.captured_devices += [device]
