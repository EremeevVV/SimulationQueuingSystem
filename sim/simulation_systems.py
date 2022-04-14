class SimulationQueuingSystem:

    def __init__(self, num_channels: int, max_queue_length:int, processing_intensity:float) -> None:
        self.income_intensity = income_intensity
        self.queue = RestrictedQueue(maxsize=max_queue_length)
        self.condition = 0
        self.request_counter = RequestCounter()


    def get_free_channel_index(self):
        for index, _ in enumerate(self.channels):
            if self.channels[index].free is False:
                return index

    def step(self, request: Request=None):
        self.condition = len([channel for channel in self.channels if channel.free]) + self.queue.qsize()
        free_channel_index = self.get_free_channel_index()

        if free_channel_index:
            if self.queue.qsize()>0:
                # брать из очереди
                from_queue = self.queue.get()
                self.channels[free_channel_index].put(from_queue)
            else:
                if request:
                    self.channels[free_channel_index].put(request)
        else:
            if request:
                try:
                    self.queue.put(request)
                except BufferError:
                    # счет отброшенных
                    pass
            else:
                pass
        for index,_ in enumerate(self.channels):
            # обработка
            # self.channels[index].step()
            pass