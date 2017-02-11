import queue

class PeekQueue(queue.Queue):
    """PeekQueue inherits from the standard thread safe Python 3 queue. The only
    difference is, that it implements additionally a peek function which was
    necessary, because the content of the queue had to be checked and depending
    on the check the pop operation had to be done. The standard queue only
    implements a get, which automatically pops the head
    """
    def __init__(self):
        super(PeekQueue, self).__init__()

    def peek(self):
        if not self.empty():
            return self.queue[0]
        else:
            return None
            