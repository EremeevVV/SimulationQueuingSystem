from sim.request import Request, generate_request
from sim.counters import RequestCounter, StateCounter
from sim.simulation_systems import SimulationQueuingSystem
from sim.timer import Timer
from sim.custom_queue import RestrictedQueue
from sim.channels import ChannelBalancer, Channel

if __name__ == '__main__':
    end_time = 150_000
    step = 0.0001
    max_queue_length = 4
    income_intensity = 4.8
    processing_intensity = 2
    num_channels = 2

    sim = SimulationQueuingSystem(queue=RestrictedQueue(max_queue_length),
                                  cb=ChannelBalancer([Channel(processing_intensity=2) for _ in range(num_channels)]),
                                  timer=Timer(current_time=.0, step_duration=step),
                                  request_counter=RequestCounter(),
                                  state_counter=StateCounter(num_channels, max_queue_length))
    # When
    for t in range(end_time):
        request = generate_request(step * income_intensity)
        sim.step(request)
    print(f'initial parameters: {step=}, {end_time=}, {income_intensity=}, {max_queue_length=}, {num_channels=}, {processing_intensity=}')
    print(f'Output results: '
          f'success Requests count = {len(sim.request_counter.success_counter)}, '
          f'rejected Requests count = {len(sim.request_counter.rejected_counter)}, '
          f'Request in queue = {sim.queue.qsize()}')
    for index, name in enumerate(sim.state_counter.states_names):
        print(f'{name} : {sim.state_counter.get_probability_be_in_state(index)}')
    print(f'Mean queue = {sim.state_counter.get_mean_queue()}, '
          f'mean busy channels = {sim.state_counter.get_mean_busy_channels()}, '
          f'mean time in queue = {sim.request_counter.get_mean_time_in_queue()}')
    print(f'абсолютная пропускная способность СМО, среднее число заявок, обслуживаемых в единицу времени = '
          f'{sim.request_counter.get_absolute_bandwidth(end_time)}')
    print(f'относительная пропускная способность, средняя доля пришедших заявок, обслуживаемых системой = '
          f'{sim.request_counter.get_relative_bandwidth()}')
    print(f'вероятность отказа, вероятность того, что заявка покинет СМО необслуженной = '
          f'{sim.request_counter.get_reject_probability()}')