from random import random

from sim.channels import Channel, ChannelBalancer
from sim.request import Request


def is_request(step:float,income_intensity:float) -> bool:
    return income_intensity * step > random()


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

    cb = ChannelBalancer(channels=[Channel(processing_intensity), Channel(processing_intensity)])
    result_lst = []
    while current_time < 1:
        request = None
        if is_request(step, income_intensity):
            request = Request(current_time)
            free_channel = cb.get_free_channel()
            if free_channel:
                free_channel.put(request)
        result = cb.step(step)
        if result:
            result_lst.extend(result)
        current_time += step
    print(result_lst)