from dataclasses import dataclass, field

from sim.request import Request


class StateCounter:
    def __init__(self, num_channels: int, max_queue_size: int) -> None:
        states_names = ['No requests']
        states_names.extend([f'{i + 1} requests in channels' for i in range(num_channels)])
        states_names.extend(
            [f'{num_channels} requests in channels and {i + 1} in queue' for i in range(max_queue_size)])
        self.states_names = tuple(states_names)
        self.counter = [0 for _ in range(num_channels + max_queue_size + 1)]
        self.num_channels = num_channels
        self.max_queue_size = max_queue_size

    def _check_null_division(self):
        if sum(self.counter) == 0:
            raise ZeroDivisionError("Can't take probability when nothing counted")

    def count(self, count_busy_channels: int, queue_size: int) -> None:
        index = count_busy_channels + queue_size
        self.counter[index] += 1

    def get_probability_be_in_state(self, index: int) -> float:
        # Вероятность нахождения системы в определенном сотоянии
        self._check_null_division()
        return self.counter[index] / sum(self.counter)

    def get_mean_queue(self):
        """When state lower than num_channels+1 don't count those steps as queue"""
        self._check_null_division()
        count_when_in_queue = sum([(state_index - self.num_channels) * self.counter[state_index] for
                                   state_index in
                                   range(self.num_channels + 1, self.max_queue_size + self.num_channels + 1)])
        return count_when_in_queue / sum(self.counter)

    def get_mean_busy_channels(self):
        """when queue exist we must count it as used all channels
        if more than one channel is used in step count it as num_used_channel * step"""
        self._check_null_division()
        count_steps_when_channel_in_use = sum(
            [state_index * self.counter[state_index] for state_index in range(self.num_channels)]) + \
                                          self.num_channels * sum(self.counter[self.num_channels:])
        return count_steps_when_channel_in_use / sum(self.counter)


@dataclass
class RequestCounter:
    success_counter: list[Request] = field(default_factory=lambda: [])
    rejected_counter: list[Request] = field(default_factory=lambda: [])

    def add_success_request(self, request: Request) -> None:
        self.success_counter.append(request)

    def add_reject_request(self, request: Request) -> None:
        self.rejected_counter.append(request)

    def get_absolute_bandwidth(self, interval: float) -> float:
        # A  –абсолютная пропускная способность СМО, среднее число заявок, обслуживаемых в единицу времени
        return len(self.success_counter) / interval

    def get_relative_bandwidth(self):
        # Q  –относительная пропускная способность, средняя доля пришедших заявок, обслуживаемых системой
        # (или вероятность того, что пришедшая заявка будет обслужена)
        return len(self.success_counter) / (len(self.success_counter) + len(self.rejected_counter))

    def get_reject_probability(self):
        # Pотказа–вероятность отказа, вероятность того, что заявка покинет СМО необслуженной
        return len(self.rejected_counter) / (len(self.success_counter) + len(self.rejected_counter))