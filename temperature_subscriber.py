# author : Group 6
# date   : December 8th, 2023
# filename: subscriber code
# description: this is a part of our final project 
#-----------------------------------------------------------------------------------------------------



import json
from tkinter import *
import paho.mqtt.client as mqtt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import paho.mqtt.client as mqtt
import tkinter as tk

root = tk.Tk()

class Subscriber:
    def __init__(self, topic='temperature'):
        self.client = mqtt.Client()
        self.client.on_message = Subscriber.message_handler
        self.client.connect('localhost', 1883)
        self.client.subscribe(topic)
        print(f'Subscriber listening to : {topic}\n...')


    @staticmethod
 
    def message_handler( client, userdata, message):
        
            data = message.payload.decode('utf-8')
            data_dict = json.loads(data)
            print('data_dict:', data_dict)

    def block(self):
        self.client.loop_forever()

sub = Subscriber()
sub.block()

