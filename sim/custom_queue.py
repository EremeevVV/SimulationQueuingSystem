from queue import Queue


class RestrictedQueue(Queue):
    def put_nowait(self, item):
        if self.full():
            raise BufferError('Queue is full')
        return self.put(item, block=False)

