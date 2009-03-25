import logging, FilterImpl

class DelWordFilter(FilterImpl.FilterImpl):
    def __init__(self, sourcePipe, sinkPipe, *wordList):

        logging.info('DelWordFilter.__init__ sourcePipe : ' + str(sourcePipe ) )
        logging.info('DelWordFilter.__init__ sinkPipe : ' + str(sinkPipe) )
        self.__wordList = wordList
        assert(None != sourcePipe)
        assert(None != sinkPipe)
        FilterImpl.FilterImpl.__init__(self, sourcePipe, sinkPipe)

    def process(self, data ): #override
        logging.debug('DelwordFilter.process()' + str(data) )
        for word in self.__wordList:
            findPos = data.find(word)
            if -1 != findPos : # find
                data = data.replace(word, '') # delete

        return data

    def isProcessPush(self, data ) : #override
        if False == FilterImpl.FilterImpl.isProcessPush(self, data ) :
            return False
        else:
            temp = data.strip()
            if '' == temp :
                return False        # not send empty line
            else:
                return True
                
