import threading

class Error:
    self.errCode
    self.errDesc

class PipesInterface:
    def push( self, data ):
        raise NotImplementedError
    def pull( self ):
        raise NotImplementedError



class ThreadFilters(threading.Thread):
    def __init__(self, sourcePipe , sinkPipe ):
        self.__sourcePipe = sourcePipe
        self.__sinkPipe = sinkPipe
        threading.Thread.__init__(self)


