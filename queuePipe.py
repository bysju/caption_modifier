import pipesAndFilters, queue

class Empty(Exception):
    pass
class Full(Exception):
    pass
class TERMINATE:        #inform finished job
    pass

class Enum:
    WORK = 0
    TERMINATE = 1

class QueuePipe(pipesAndFilters.PipesInterface):
    def __init__(self):
        self.__queue = queue.Queue()        #thread safe
        self.__state = Enum.WORK

    def push( self, data):
        try:
            self.__queue.put(data)
        except queue.Full:
            raise Full

    def pull( self ):
        data = self.__queue.get()       #block if queue is empty
            return data
    
