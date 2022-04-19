from dataclasses import dataclass
from random import random
from typing import Optional


@dataclass
class Request:
    create_time: float = 0
    time_in_queue: float = 0
    time_in_processing: float = 0
    used_channel_index: Optional[int] = None


def generate_request(income_intensity_in_step:float) -> Request:
    if income_intensity_in_step > random():
        return Request()