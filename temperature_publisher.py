# author : Group 6
# date   : December 8th, 2023
#filename: publisher code 
#description: this is a part of our final project 
#-----------------------------------------------------------------------------------------------------

import json
import time
import paho.mqtt.client as mqtt
from tkinter import Tk, Label, Button, Entry, ttk
from random import randint, choice, uniform
from Temperature_generator import TemperatureGenerator

class TemperaturePublisherGUI:
    def __init__(self, publisher_id):
        self.root = Tk()
        self.root.title(f'Centennial College - Temperature Publisher ID {publisher_id}')
        self.root.configure(bg='pink') 

        self.broker_host = 'localhost'
        self.broker_port = 1883
        self.topic = 'temperature'
        self.interval = 3000
        self.publisher_id = publisher_id

        self.temperature_generator = TemperatureGenerator()
        self.mqtt_client = mqtt.Client()

    
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 14, 'bold'), background='pink')


        self.heading_label = Label(self.root, text='Centennial College', bg='pink', fg='black', font=('Arial', 18, 'bold'))
        self.heading_label.pack(pady=10)
        self.line_label = ttk.Label(self.root, text='__________________', font=('Arial', 1), background='pink')
        self.line_label.pack(pady=5)


        self.start_button = ttk.Button(self.root, text='Start', command=self.start_publishing)
        self.start_button.pack(pady=10)


        self.stop_button = ttk.Button(self.root, text='Stop', command=self.stop_publishing, state='disabled')
        self.stop_button.pack(pady=10)

 
        self.set_topic_label = Label(self.root, text='Set Topic:', bg='pink', font=('Arial', 12, 'bold'))
        self.set_topic_label.pack()
        self.topic_entry = Entry(self.root, font=('Arial', 12))
        self.topic_entry.insert(0, self.topic)
        self.topic_entry.pack(pady=10)

        self.set_interval_label = Label(self.root, text='Set Interval (ms):', bg='pink', font=('Arial', 12, 'bold'))
        self.set_interval_label.pack(pady=10)
        self.interval_entry = Entry(self.root, font=('Arial', 12))
        self.interval_entry.insert(0, str(self.interval))
        self.interval_entry.pack(pady=10)


        self.set_topic_button = ttk.Button(self.root, text='Set Topic', command=self.set_topic)
        self.set_topic_button.pack(pady=10)

        self.after_id = None

    def start_publishing(self):
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.mqtt_client.connect(host=self.broker_host, port=self.broker_port)
        self.mqtt_client.loop_start()
        self.publish_data()

    def stop_publishing(self):
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.mqtt_client.loop_stop()
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        print(f'Publisher ID {self.publisher_id}: Publishing stopped.')

    def set_topic(self):
        self.topic = self.topic_entry.get()
        print(f'Publisher ID {self.publisher_id}: Topic set to: {self.topic}')

    def publish_data(self):
        if randint(1, 100) == 1:
            data_point = self.generate_wild_data()
        else:
            data_point = self.generate_data_point()

        data_json = json.dumps(data_point, indent=2)
        self.mqtt_client.publish(topic=self.topic, payload=data_json, qos=0)
        print(f'Publisher ID {self.publisher_id}: Published: {data_json}')

        self.interval = int(self.interval_entry.get())
        self.after_id = self.root.after(self.interval, self.publish_data)

    def generate_data_point(self):
        temperature = self.temperature_generator.temperature
        city = choice(['Toronto', 'Montreal', 'New York', 'Vancouver', 'Seoul'])
        data_point = {'time': self.format_time(time.time()), 'temperature': round(temperature, 2), 'city': city}
        return data_point

    def generate_wild_data(self):
        data_point = {'time': self.format_time(time.time()), 'temperature': round(uniform(-100, 100), 2), 'city': 'Unknown'}
        return data_point

    def format_time(self, timestamp):
        formatted_time = time.strftime('%H:%M:%S', time.localtime(timestamp))
        return formatted_time

    def run_gui(self):
        self.root.geometry('400x400')
        self.root.mainloop()

if __name__ == '__main__':
    num_publishers = 3
    publishers = [TemperaturePublisherGUI(publisher_id=i) for i in range(num_publishers)]

    for publisher in publishers:
        publisher.run_gui()
