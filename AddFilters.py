import logging, FilterImpl, const

const.STATE_FIND_START = 0
const.STATE_FIND_END   = 1

class DelWordFilter(FilterImpl.FilterImpl):
    def __init__(self, sourcePipe, sinkPipe, *wordList):

        logging.info('DelWordFilter.__init__ sourcePipe : ' + str(sourcePipe ) )
        logging.info('DelWordFilter.__init__ sinkPipe : ' + str(sinkPipe) )
        self.__wordList = wordList
        assert(None != sourcePipe)
        assert(None != sinkPipe)
        FilterImpl.FilterImpl.__init__(self, sourcePipe, sinkPipe)

    def process(self, data ): #override
        try:
            logging.debug('DelwordFilter.process()' + str(data) )
            for word in self.__wordList:
                findPos = data.find(word)
                if -1 != findPos : # find
                    data = data.replace(word, '') # delete

            return data
        except BaseException as err:
            return err
    def isProcessPush(self, data ) : #override
        if False == FilterImpl.FilterImpl.isProcessPush(self, data ) :
            return False
        else:
            temp = data.strip()
            if '' == temp :
                return False        # not send empty line
            else:
                return True


class DelRangeFilter(FilterImpl.FilterImpl):
    def __init__(self, sourcePipe, sinkPipe, startTag, endTag ):
        logging.info('DelRangeFilter.__init__ sourcePipe : ' + str(sourcePipe ) )
        logging.info('DelRangeFilter.__init__ sinkPipe : ' + str(sinkPipe) )
        self.__startTag = startTag
        self.__endTag = endTag
        self.__state = const.STATE_FIND_START
        assert(None != sourcePipe)
        assert(None != sinkPipe)
        FilterImpl.FilterImpl.__init__(self, sourcePipe, sinkPipe)

    def beforeProcess(self, data) : #override
        logging.debug('DelRangeFilter.beforeProcess()' + str(data) )
        self.__startPos = 0
        self.__reRead = True    # re read data
        return FilterImpl.FilterImpl.beforeProcess(self, data )

    def isProcessPush( self, data ) : #override
        if False == FilterImpl.FilterImpl.isProcessPush(self, data ) :
            return False
        else:
            temp = data.strip()
            if '' == temp :
                return False        # not send empty line
            else:
                return True

    def process(self, data ) : #override
        try:
            while True :
                if const.STATE_FIND_START == self.__state :
                    
                    findPos = data.find( self.__startTag, self.__startPos )

                    if -1 == findPos :
                        return data              # if not found nothing to do
                    else:
                        self.__startPos = findPos
                        self.__state = const.STATE_FIND_END
                        self.__reRead = False
                        continue
                    
                elif const.STATE_FIND_END == self.__state:

                    if False == self.__reRead:
                        findPos = self.__startPos + len(self.__startTag)
                    else:
                        findPos = self.__startPos
                    endPos = data.find( self.__endTag , findPos )

                    if -1 != endPos : # find
                        data = data[:self.__startPos] + data[ (endPos + len(self.__endTag) ):]
                        self.__startPos = 0
                        self.__state = const.STATE_FIND_START
                        continue        #re find
                    else :              # not found
                        data = data[:self.__startPos]
                        return data          # read next data
            
        except BaseException as err:
            return err
                
