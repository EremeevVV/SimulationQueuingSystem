import math
from copy import copy, deepcopy
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

    def put(self, request: Request) -> Optional[Request]:
        if self.free:
            self.free = False
            self.processing_time = self._generate_processing_time()
            self.request = request
            self.request.time_in_processing = self.processing_time
            return self.request
        else:
            raise BufferError('Channel is busy')

    def step(self, step_time: float) -> None:
        self.processing_time -= step_time
        if self.processing_time <= 0:
            self.request = None
            self.free = True

class ChannelBalancer:

    def __init__(self, channels: list[Channel]) -> None:
        if len(channels)<1:
            raise ValueError('There are must be at least one channel')
        self.channels = channels

    def check_available_channels(self) -> bool:
        for channel in self.channels:
            if channel.free:
                return True
        return False

    def put(self, request: Request) -> Request:
        """Put request in available channel"""
        for index, channel in enumerate(self.channels):
            if channel.free:
                request.used_channel_index = index
                return channel.put(request)
        else:
            raise BufferError('There are no available channels')

    def step(self, step_time: float) -> None :
        """If in one step come more then one result"""
        for channel in self.channels:
            if channel.free is False:
                channel.step(step_time)



