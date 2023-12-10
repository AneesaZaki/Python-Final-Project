# author : Group 6
# date   : December 8th, 2023
# filename: data generator code
# description: this is a part of our final project 
#-----------------------------------------------------------------------------------------------------

import random
import time

class TemperatureGenerator:
    def __init__(self, base_temperature=20):
        self.base_temperature = base_temperature
        self._data = 0
        self.random_dict = {
            'value': random.randint(3, 7) / 10,
            'delta': 0.004,
            'cycle': 0
        }

    @property
    def temperature(self):
        self._data = self._get_random()
        return self.base_temperature + (self._data * 10)

    def _get_random(self):

        if self.random_dict['cycle'] == 0:
            self.random_dict['cycle'] = random.randint(2, 8) * 10
            self.random_dict['delta'] *= -1
        self.random_dict['cycle'] -= 1
        self.random_dict['value'] += self.random_dict['delta']


        self.random_dict['value'] += random.randint(-30, 30) / 1000


        if self.random_dict['value'] < 0:
            self.random_dict['delta'] = abs(self.random_dict['delta'])
            self.random_dict['value'] = random.randint(50, 150) / 1000
        if self.random_dict['value'] > 1:
            self.random_dict['delta'] = abs(self.random_dict['delta']) * -1
            self.random_dict['value'] = random.randint(850, 950) / 1000

        return round(self.random_dict['value'], 2)


class TemperatureDataGenerator:
    def __init__(self):
        self.temperature_generator = TemperatureGenerator()
        self.cities = ['Toronto', 'Montreal', 'New York', 'Vancouver', 'Seoul']

    def generate_data_point(self):
        timestamp = int(time.time())
        temperature = self.temperature_generator.temperature
        city = random.choice(self.cities)
        data_point = {'time': timestamp, 'temperature': round(temperature, 2), 'city': city}
        return data_point

if __name__ == '__main__':
    data_generator = TemperatureDataGenerator()

    for _ in range(10):
        data_point = data_generator.generate_data_point()
        print(data_point)
        time.sleep(1)
