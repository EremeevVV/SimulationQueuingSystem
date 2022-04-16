from dataclasses import dataclass, field
from random import random
from typing import Optional, Callable


@dataclass
class Request:
    create_time: float = 0
    time_in_queue: float = 0
    time_in_processing: float = 0
    used_channel_index: Optional[int] = None

@dataclass
class RequestCounter:
    success_counter: list[Request] = field(default_factory=lambda: [])
    rejected_counter: list[Request] = field(default_factory=lambda: [])

    def add_success_request(self, request:Request) -> None:
        self.success_counter.append(request)

    def add_reject_request(self, request:Request) -> None:
        self.rejected_counter.append(request)


def generate_request(income_intensity_in_step:float) -> Request:
    if income_intensity_in_step > random():
        return Request()