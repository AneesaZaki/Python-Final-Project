# author : Group 6
# date   : December 8th, 2023
# filename: subscriber gui 
# description: this is a part of our final project 
#-----------------------------------------------------------------------------------------------------


import numpy as np
import paho.mqtt.client as mqtt
import json
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SubscriberGUI:
    def __init__(self, broker_address='localhost', qos=0):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_address = broker_address
        self.qos = qos
        self.root = tk.Tk()
        self.root.title('MQTT Subscriber')
        self.root.geometry('800x600')

        # Entry for topic text area 
        self.topic_entry_label = tk.Label(self.root, text='Please Enter MQTT Topic:')
        self.topic_entry_label.pack(side=tk.TOP, pady=5)
        self.topic_entry = tk.Entry(self.root)
        self.topic_entry.pack(side=tk.TOP, pady=5)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.x_data = []
        self.y_data = []
        self.is_running = False

        # This is where i put the coding for the Start button
        self.start_button = tk.Button(self.root, text='Start', command=self.start_update)
        self.start_button.pack(side=tk.LEFT, padx=10)

        # This is where i put the coding for the Stop button
        self.stop_button = tk.Button(self.root, text='Stop', command=self.stop_update)
        self.stop_button.pack(side=tk.LEFT)

    def on_connect(self, client, userdata, flags, rc):
        print('Connected with result code ' + str(rc))
        client.subscribe(self.topic_entry.get(), qos=self.qos)

    def on_message(self, client, userdata, msg):
        if self.is_running:
            data = json.loads(msg.payload.decode('utf-8'))
            print(f"Received message '{data}' on topic '{msg.topic}'")
            self.process_data(data)
            self.root.after(100, lambda: self.update_plot(data))

    def process_data(self, data):
        time_str = data.get('time', '')

        time_seconds = sum(int(x) * 60**i for i, x in enumerate(reversed(time_str.split(':'))))
        self.x_data.append(time_seconds)
        self.y_data.append(data.get('temperature', 0))

    def update_plot(self, data):
        self.ax1.clear()


        y_hours = np.array(self.x_data) / 3600.0  # 3600 seconds in an hour

        self.ax1.plot(self.y_data, y_hours, marker='o', linestyle='-', label='Temperature')
        self.ax1.set_title('Temperature GUI: ' + str(data.get('id', '')))
        self.ax1.set_xlabel('Temperature')
        self.ax1.set_ylabel('Time (hours)')
        self.ax1.set_xlim([18, 28])

        self.ax1.set_yticks([4, 8, 12, 16, 20, 24])

        self.ax1.legend()
        self.canvas.draw()

    def start_update(self):
        self.is_running = True
        self.client.connect(self.broker_address, 1883, 60)
        self.client.loop_start()

    def stop_update(self):
        self.is_running = False

    def run(self):
        self.root.mainloop()

sub = SubscriberGUI()
sub.run()
