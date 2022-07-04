import socket
from threading import Thread
import ui
from capture_receiver import *

receiver = Receiver(["kali-pi-1", "kali-pi-2", "kali-pi-4"])
ui = ui.Ui(receiver)


def start_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ("192.168.0.127", 8889)
    sock.bind(address)
    print("Starting capture loop ...")
    while True:
        data, addr = sock.recvfrom(1024)
        data = data.decode('UTF-8')
        address, sniffer, rssi = data.split(" ")[0], data.split(" ")[1], data.split(" ")[2]
        receiver.receive_capture(address, sniffer, rssi)
        # print(data)


socket_thread = Thread(target=start_socket)
socket_thread.start()
ui.start()


# TODO Remove devices from detected when moved to present
# TODO fix rssi locating when device move in/out room
