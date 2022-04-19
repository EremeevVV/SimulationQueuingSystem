from sim.request import Request, generate_request
from sim.counters import RequestCounter
from sim.simulation_systems import SimulationQueuingSystem
from sim.timer import Timer
from sim.custom_queue import RestrictedQueue
from sim.channels import ChannelBalancer, Channel


def test_one_step():
    # Given
    step_time = 0.001
    max_queue_length = 4
    num_channels = 2
    sim = SimulationQueuingSystem(queue=RestrictedQueue(max_queue_length),
                                  cb=ChannelBalancer([Channel(processing_intensity=2) for _ in range(num_channels)]),
                                  timer=Timer(current_time=.0, step_duration=step_time),
                                  request_counter=RequestCounter())
    request = Request(0.1)
    # When
    sim.step(request)
    assert sim.request_counter.success_counter[0].create_time == request.create_time


def test_queue_in_step():
    # Given
    step_time = 0.01
    income_intensity = 4.8
    max_queue_length = 4
    num_channels = 2
    sim = SimulationQueuingSystem(queue=RestrictedQueue(max_queue_length),
                                  cb=ChannelBalancer([Channel(processing_intensity=2) for _ in range(num_channels)]),
                                  timer=Timer(current_time=.0, step_duration=step_time),
                                  request_counter=RequestCounter())
    # When
    for t in range(150):
        request = generate_request(step_time * income_intensity)
        sim.step(request)
    print(sim.request_counter)


if __name__ == '__main__':
    test_one_step()
    test_queue_in_step()
