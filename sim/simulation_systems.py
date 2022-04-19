from dataclasses import dataclass

from sim.channels import ChannelBalancer
from sim.custom_queue import RestrictedQueue
from sim.request import Request
from sim.counters import RequestCounter, StateCounter
from sim.timer import Timer


@dataclass
class SimulationQueuingSystem:

    queue: RestrictedQueue
    cb: ChannelBalancer
    request_counter: RequestCounter
    state_counter: StateCounter
    timer: Timer

    def step(self, request: Request = None):

        if self.cb.check_available_channels():
            try:
                from_queue = self.queue.get_nowait()
                try:
                    result = self.cb.put(from_queue)
                    result.time_in_queue = self.timer.get_current_time() - result.create_time
                    self.request_counter.add_success_request(result)
                except BufferError:
                    raise Exception(
                        f'{from_queue} did not put in ChannelBalancer when available channel status is {self.cb.check_available_channels()}')
            except BufferError:
                #  Queue is empty and no request
                pass

        if request:
            request.create_time = self.timer.get_current_time()
            if self.queue.qsize() < 1:
                try:
                    result = self.cb.put(request)
                    if result:
                        self.request_counter.add_success_request(result)
                except BufferError:
                    self.queue.put_nowait(request)
            else:
                try:
                    self.queue.put_nowait(request)
                except BufferError:
                    self.request_counter.add_reject_request(request)
        self.state_counter.count(count_busy_channels = self.cb.count_busy(), queue_size = self.queue.qsize())
        self.cb.step(self.timer.step_duration)
        self.timer.step()
