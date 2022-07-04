import datetime
from tkinter import *
from tkinter import ttk


class Ui(object):

    def __init__(self, receiver):
        self.window = Tk()
        self.top_frame = ttk.Frame(self.window, height=100, width=900)
        self.present_frame_style = ttk.Style()
        self.present_label_style = ttk.Style()
        self.present_label_header_style = ttk.Style()
        self.present_label_header_style.configure("PresentHeader.TLabel", background='black', foreground='white')
        self.present_frame_style.configure("Present.TFrame", background='black', foreground='silver')
        self.present_label_style.configure("present.TLabel", background='black', foreground='silver')
        self.present_devices_frame = ttk.Frame(self.window, style="Present.TFrame", padding=20, borderwidth=1,
                                               relief=RIDGE)
        self.detected_devices_frame = ttk.Frame(self.window, padding=20)
        self.bottom_frame = ttk.Frame(self.window, padding=20)
        self.receiver = receiver

    def start(self):

        self.top_frame.grid()
        self.present_devices_frame.grid()
        ttk.Label(self.present_devices_frame, text="Address", style="PresentHeader.TLabel").grid(row=0, column=0)
        ttk.Label(self.present_devices_frame, text="Vendor", style="PresentHeader.TLabel").grid(row=0, column=1)
        ttk.Label(self.present_devices_frame, text="RSSI", style="PresentHeader.TLabel").grid(row=0, column=2)
        ttk.Label(self.present_devices_frame, text="Count", style="PresentHeader.TLabel").grid(row=0, column=3)
        self.detected_devices_frame.grid()
        ttk.Label(self.detected_devices_frame, text="Found devices").grid(row=0, column=0)
        self.bottom_frame.grid()

        def update():

            for widget in self.present_devices_frame.winfo_children():
                widget.destroy()
            for widget in self.detected_devices_frame.winfo_children():
                widget.destroy()

            ttk.Label(self.present_devices_frame, text="Address", style="PresentHeader.TLabel").grid(row=0, column=0)
            ttk.Label(self.present_devices_frame, text="Vendor", style="PresentHeader.TLabel").grid(row=0, column=1)
            ttk.Label(self.present_devices_frame, text="RSSI", style="PresentHeader.TLabel").grid(row=0, column=2)
            ttk.Label(self.present_devices_frame, text="Count", style="PresentHeader.TLabel").grid(row=0, column=3)

            present_devices = [device for device in self.receiver.devices if device.check_in(
                self.receiver.get_in_sniffers_indexes())]

            ttk.Label(self.top_frame, text="Present devices: " + str(len(present_devices))).grid(column=0,
                                                                                                 row=0,
                                                                                                 columnspan=3,
                                                                                                 sticky='W')

            for sniffer, index in zip(self.receiver.sniffers, range(len(self.receiver.sniffers))):
                ttk.Button(self.top_frame, text=sniffer.name, command=sniffer.set_in_out).grid(row=1, column=index)

            for device, index in zip(present_devices, range(len(present_devices))):
                ttk.Label(self.present_devices_frame, text=device.address, style="present.TLabel").grid(row=index + 1,
                                                                                                        column=0)
                ttk.Label(self.present_devices_frame, text=device.vendor, style="present.TLabel").grid(row=index + 1,
                                                                                                       column=1)
                ttk.Label(self.present_devices_frame, text=max(device.rssi), style="present.TLabel").grid(row=index + 1,
                                                                                                          column=2)
                ttk.Label(self.present_devices_frame, text=device.count, style="present.TLabel").grid(row=index + 1,
                                                                                                      column=3)

            detected_devices = [device for device in self.receiver.devices if not device.check_in(
                self.receiver.get_in_sniffers_indexes())]

            # for device, index in zip(detected_devices, range(len(detected_devices))):
                # ttk.Label(self.detected_devices_frame, text=device.address, style="present.TLabel").grid(row=index + 1,
                                                                                                        # column=0)

            for sniffer in self.receiver.sniffers:
                _, sniffer_index = self.receiver.get_sniffer(sniffer.name)
                new_frame = ttk.Frame(self.detected_devices_frame, relief='sunken', padding=2)
                new_frame.grid(row=0, column=sniffer_index)
                ttk.Label(new_frame, text=sniffer.name).grid(row=0, column=0)
                for device, index in zip(sniffer.captured_devices, range(len(sniffer.captured_devices))):
                    ttk.Label(new_frame, text=device.get_address()).grid(row=index+1, column=0)
                    ttk.Label(new_frame, text=device.rssi[sniffer_index]).grid(row=index + 1, column=1)

            ttk.Label(self.bottom_frame, text=datetime.datetime.now().strftime('%H:%M:%S')).grid(row=3, column=0)

            self.receiver.snapshot()
            self.window.after(1000, update)

        update()
        self.window.mainloop()
