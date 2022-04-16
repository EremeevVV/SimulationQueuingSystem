from dataclasses import dataclass


@dataclass
class Timer:
    current_time: float
    step_duration: float

    def step(self):
        self.current_time += self.step_duration

    def get_current_time(self):
        return self.current_time
