

class PipesInterface:
    def push( self, data ):
        raise NotImplementedError
    def pull( self ):
        raise NotImplementedError



class FiltersInterface:
    def __init__(self, sourcePipe = None, sinkPipe = None ):
        self.__sourcePipe = sourcePipe
        self.__sinkPipe = sinkPipe
