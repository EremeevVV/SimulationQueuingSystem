from dataclasses import dataclass, field
from random import random
from enum import Enum
import math
from queue import Queue
from typing import Callable
from urllib import request

import scipy.stats as sps


@dataclass
class Request:
    create_time: float
    time_in_queue: float = 0
    time_in_processing: float = 0

@dataclass
class RequestCounter:
    success_counter: list[Request] = field(default_factory=lambda: [])
    rejected_counter: list[Request] = field(default_factory=lambda: [])

    def add_success_request(self, request:Request) -> None:
        self.success_counter.append(request)

    def add_reject_request(self, request:Request) -> None:
        self.rejected_counter.append(request)


class Channel:
    free: bool = True
    processing_time: float

    def __init__(self, processing_intensity: float, distribution_function: Callable = None) -> None:
        if distribution_function is None:
            distribution_function = lambda x: (-1 / x) * math.log(1 - random(), math.e)
        self.distribution_function = distribution_function
        self.processing_intensity = processing_intensity
        self.request = None

    def _generate_processing_time(self):
        return self.distribution_function(self.processing_intensity)

    def put(self, request:Request):
        self.free = False
        self.processing_time = self._generate_processing_time()
        self.request = request
        self.request.time_in_processing = self.processing_time

    def step(self, step_time: float):
        self.processing_time -= step_time
        if self.processing_time <= 0:
            self.free = True
            return self.request

class ChannelBalancer:

    def __init__(self, channels: list[Channel]) -> None:
        if len(channels)<1:
            raise ValueError('There are must be at least one channel')
        self.channels = channels

    def get_free_channel(self):
        for channel in self.channels:
            if channel.free:
                return channel

class RestrictedQueue(Queue):
    def put_nowait(self, item):
        if self.full():
            raise BufferError('Queue is full')
        return self.put(item, block=False)


class SimulationQueuingSystem:

    def __init__(self, num_channels: int, max_queue_length:int, processing_intensity:float) -> None:
        self.income_intensity = income_intensity
        self.queue = RestrictedQueue(maxsize=max_queue_length)
        self.condition = 0
        self.request_counter = RequestCounter()


    def get_free_channel_index(self):
        for index, _ in enumerate(self.channels):
            if self.channels[index].free is False:
                return index

    def step(self, request: Request=None):
        self.condition = len([channel for channel in self.channels if channel.free]) + self.queue.qsize()
        free_channel_index = self.get_free_channel_index()

        if free_channel_index:
            if self.queue.qsize()>0:
                # брать из очереди
                from_queue = self.queue.get()
                self.channels[free_channel_index].put(from_queue)
            else:
                if request:
                    self.channels[free_channel_index].put(request)
        else:
            if request:
                try:
                    self.queue.put(request)
                except BufferError:
                    # счет отброшенных
                    pass
            else:
                pass
        for index,_ in enumerate(self.channels):
            # обработка
            # self.channels[index].step()
            pass


def is_request(step:float,income_intensity:float) -> bool:
    return income_intensity * step > random()



# income_rv = sps.expon(scale=income_mean_time)
# outcome_rv = sps.expon(scale=processing_mean_time)

if __name__ == '__main__':
    channel_count = 2
    step = 0.0001
    max_queue_length = 4
    income_intensity = 4.8
    processing_intensity = 2
    income_mean_time = 1 / income_intensity
    processing_mean_time = 1 / processing_intensity
    # smo = SimulationQueuingSystem(num_channels=2, max_queue_length=4, processing_intensity=2)
    current_time = 0
    channel1 = Channel(processing_intensity)
    channel2 = Channel(processing_intensity)
    cb = ChannelBalancer(channels=[channel1, channel2])
    result_lst = []
    while current_time < 1:
        request = None
        if is_request(step,income_intensity):
            request = Request(current_time)
            if channel.free:
                channel.put(request)
        if channel.free is False:
            result = channel.step(step)
            if result:
                result_lst.append(result)
        current_time += step
    print(result_lst)