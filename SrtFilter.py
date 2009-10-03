import logging, FilterImpl, const

const.STATE_SEQ    = 0
const.STATE_TIME   = 1
const.STATE_DATA   = 2
const.STATE_BLANK  = 3

const.TIME_ARROW   = '-->'
const.TIME_COLON   = ':'
const.TIME_COMMA   = ','

class SrtFilter(FilterImpl.FilterImpl):
    def __init__(self, sourcePipe, sinkPipe, lastSeq ):
        logging.info('SrtFilter.__init__ sourcePipe : ' + str(sourcePipe) )
        logging.info('SrtFilter.__init__ sinkPipe : ' + str(sinkPipe ))
        self.__lastSeq = lastSeq
        self.__beforeSeq = 0
        assert(None != sourcePipe)
        assert(None != sinkPipe )
        FilterImpl.FilterImpl.__init__(self, sourcePipe, sinkPipe)

        

    def process(self , data): # override
        try:
            state = self.__getState( data )
            logging.debug( str( state) )
            logging.debug(data)

            if const.STATE_DATA == state :
                return data
            else:
                return None
            
                        
        except BaseException as err:
            logging.error( "SrtFilter errr " + str(err) )
            return err

    def isProcessPush(self, data ): #override
        if False == FilterImpl.FilterImpl.isProcessPush(self, data) :
            return False
        else:
            if None == data :
                return False        # not send blank or time info
            else:
                return True

    def __getState(self, data):
        result = data.strip()
        if '' == result:
            return const.STATE_BLANK
        elif result.isdigit():
            return const.STATE_SEQ
        elif -1 != result.find(const.TIME_ARROW ):
            result = result.replace(const.TIME_ARROW, '') #delete
            result = result.replace(const.TIME_COLON, '') #delete
            result = result.replace(const.TIME_COMMA, '') #delete
            result = result.replace(' ' , '') # delete center space
            if result.strip().isdigit():
                return const.STATE_TIME
            else:
                return const.STATE_DATA
        else:
            return const.STATE_DATA
            
            
        
