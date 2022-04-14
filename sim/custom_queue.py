from queue import Queue


class RestrictedQueue(Queue):
    def put_nowait(self, item):
        if self.full():
            raise BufferError('Queue is full')
        return self.put(item, block=False)

    def get_nowait(self):
        if self.empty():
            raise BufferError('Queue is empty')
        return self.get(block=False)
