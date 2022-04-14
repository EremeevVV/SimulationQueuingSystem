from sim.channels import Channel, ChannelBalancer
from sim.custom_queue import RestrictedQueue
from sim.request import RequestCounter, Request


class SimulationQueuingSystem:

    def __init__(self, num_channels: int, max_queue_length:int, processing_intensity:float) -> None:
        self.queue = RestrictedQueue(maxsize=max_queue_length)
        self.cb = ChannelBalancer([Channel(processing_intensity) for _ in range(num_channels)])
        self.request_counter = RequestCounter()

    def step(self, request: Request=None):

        if request:
            if self.queue.qsize() < 1:
                try:
                    result = self.cb.put(request)
                except BufferError:
                    self.queue.put(request)
            else:
                try:
                    self.queue.put(request)
                except BufferError:
                    self.request_counter.add_reject_request(request)

