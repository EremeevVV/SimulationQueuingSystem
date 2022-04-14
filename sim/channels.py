import math
from random import random
from typing import Callable, Optional

from sim.request import Request


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

    def put(self, request: Request):
        if self.free:
            self.free = False
            self.processing_time = self._generate_processing_time()
            self.request = request
            self.request.time_in_processing = self.processing_time
        else:
            raise BufferError('Channel is busy')

    def step(self, step_time: float) -> Optional[Request]:
        self.processing_time -= step_time
        if self.processing_time <= 0:
            if self.free:
                self.request = None
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

    def step(self, step_time: float) -> list[Request]:
        """If in one step come more then one result"""
        finished_requests_lst = []
        finished_request = None
        for channel in self.channels:
            if channel.free is False:
                finished_request = channel.step(step_time)
            if finished_request:
                finished_requests_lst.append(finished_request)
        return finished_requests_lst


