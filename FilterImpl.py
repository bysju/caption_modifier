import threading, logging

class TERMINATE: pass

class FilterImpl(threading.Thread):
    def __init__(self, sourcePipe, sinkPipe):
        self.__sourcePipe = sourcePipe
        self.__sinkPipe = sinkPipe
        threading.Thread.__init__(self)

    def run(self):
        logging.info('FilterImpl.run()')
        while True:
            data= None
            if self.isProcessPull() :
                data = self.pull()

            if self.beforeProcess(data) :
                data = self.process(data)
                self.afterProcess(data)

            if self.isProcessPush(data) :
                self.push(data)

            if self.isError(data):
                if None != self.__sinkPipe:
                    self.push(data)
                if self.procesError(data):
                    return

            if self.isFinish(data) :
                self.finish()
                return                      #finish loop

    def pull(self):         # get data
        return self.__sourcePipe.get()

    def push(self, data):    # put data
        self.__sinkPipe.put(data)

    def finish(self ):      # put terminate class
        logging.info("FilterImpl.finish()")
        if None != self.__sinkPipe :
            self.push( TERMINATE() )

    def isProcessPull(self):
        if None == self.__sourcePipe:
            return False
        else:
            return True

    def isProcessPush(self, data):
        if None == self.__sinkPipe or self.isTerminate(data) :
            return False
        else:
            return True

    def beforeProcess(self, data ):
        if self.isTerminate(data) :
            return False
        else:
            return True

    def process(self, data ):
        return data
    
    def afterProcess(self, data ) : pass

    def processError(self, data ):
        return True

    def isFinish(self, data ):
        if self.isTerminate(data) :
            return True
        else:
            return False

    def isTerminate(self, data):
        if isinstance( data, TERMINATE ) :
            return True
        else:
            return False

    def isError(self, data):
        if isinstance( data, BaseException ) :
            return True
        else:
            return False
        
                
