from random import random

from sim.request import Request, generate_request
from sim.counters import RequestCounter
from sim.simulation_systems import SimulationQueuingSystem
from sim.timer import Timer
from sim.custom_queue import RestrictedQueue
from sim.channels import ChannelBalancer, Channel





if __name__ == '__main__':

    step = 0.0001
    max_queue_length = 4
    income_intensity = 4.8
    processing_intensity = 2
    num_channels = 2

    sim = SimulationQueuingSystem(queue=RestrictedQueue(max_queue_length),
                                  cb=ChannelBalancer([Channel(processing_intensity=2) for _ in range(num_channels)]),
                                  timer=Timer(current_time=.0, step_duration=step),
                                  request_counter=RequestCounter())
    # When
    for t in range(150000):
        request = generate_request(step * income_intensity)
        sim.step(request)




