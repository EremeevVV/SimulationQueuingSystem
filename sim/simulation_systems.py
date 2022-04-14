from random import random

from sim.channels import Channel, ChannelBalancer
from sim.custom_queue import RestrictedQueue
from sim.request import RequestCounter, Request


def is_request(step:float,income_intensity:float) -> bool:
    return income_intensity * step > random()


class SimulationQueuingSystem:

    def __init__(self, num_channels: int, max_queue_length: int, processing_intensity: float) -> None:
        self.queue = RestrictedQueue(maxsize=max_queue_length)
        self.cb = ChannelBalancer([Channel(processing_intensity) for _ in range(num_channels)])
        self.request_counter = RequestCounter()
        self.current_time = 0


    def step(self, step_time: float, request: Request = None):

        if request:
            if self.queue.qsize() < 1:
                try:
                    result = self.cb.put(request)
                    self.request_counter.add_success_request(result)
                except BufferError:
                    self.queue.put_nowait(request)
            else:
                try:
                    self.queue.put_nowait(request)
                except BufferError:
                    self.request_counter.add_reject_request(request)

        if self.cb.check_available_channels():
            try:
                from_queue = self.queue.get_nowait()
                try:
                    result = self.cb.put(from_queue)
                    result.time_in_queue = self.current_time - result.create_time
                    self.request_counter.add_success_request(result)
                except BufferError:
                    raise Exception(
                        f'{from_queue} did not put in ChannelBalancer when available channel status is {self.cb.check_available_channels()}')
            except BufferError:
                #  Queue is empty and no request
                pass
        self.cb.step(step_time)

    def cycle(self, step: float, income_intensity: float, start_time: float = .0, end_time: float = .0) -> None:
        self.current_time = start_time
        while self.current_time < end_time:
            if is_request(step, income_intensity):
                request = Request(self.current_time)
            else:
                request = None
            self.step(step, request)
            self.current_time += step
