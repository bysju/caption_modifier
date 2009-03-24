import  threading, logging

class TERMINATE:
    pass

class Error:
    errCode = 0
    errDesc = ""

class STATE_ENUM:
    FIND_STARTTAG = 0
    FIND_ENDTAG = 1

class ERORR_CODE:
    TAG_NOT_MATCH = 0

error = Error()

class SrcFileFilter(threading.Thread):
    def __init__(self, sinkPipe , sourceFile):
        self.__sinkPipe = sinkPipe
        logging.info("SrcFileFilter.__init__ " + str(sinkPipe) )
        logging.info("SrcFileFilter.__init__ read File (%s)" % sourceFile )
        self.__file = open(sourceFile)
        threading.Thread.__init__(self)
        assert(None != sinkPipe)
    def run(self):      # run provieds thread logic
        logging.info('SrcFileFilter.run')
        #read file
        lines = self.__file.readlines()
        
        for line in lines:
            logging.debug ('SrcFileFilter:run '+ line)
            self.__sinkPipe.put(line)  #push file data
        logging.info('SrcFileFilter:run finish job')
        self.__sinkPipe.put( TERMINATE())  #terminate job

class SinkFileFilter(threading.Thread):
    def __init__(self, sourcePipe , sinkFile ):
        self.__sourcePipe = sourcePipe
        logging.info("SinkFileFilter.__init__ " + str(sourcePipe) )
        self.__file = open(sinkFile, 'w')
        assert(None != sourcePipe)
        threading.Thread.__init__(self)
    def run(self):
        
        logging.info('SinkFileFilter.run')
        while True:
            data = self.__sourcePipe.get()
            if isinstance( data, TERMINATE ) :
                logging.info('SinkFileFilter:run finish')
                return      #finish job
            logging.debug('SinkFileFilter:run input data '+ data )
            self.__file.write(data)


class DelTagFilter(threading.Thread):
    def __init__(self,  sourcePipe, sinkPipe, *tagList ):
        self.__sourcePipe = sourcePipe
        self.__sinkPipe = sinkPipe

        logging.info('DelTagFilter.__init__ sourcePipe : ' + str(sourcePipe ) )
        logging.info('DelTagFilter.__init__ sinkPipe : ' + str(sinkPipe) )
        self.__tagList = tagList
        assert(None != sourcePipe)
        assert(None != sinkPipe)
        self.__endTag = '>'
        self.__state = STATE_ENUM.FIND_STARTTAG
        self.__startTagPosition  = 0                # location of start tag
        self.__endTagPosition    = 0               # location of end tag
        threading.Thread.__init__(self)

    def run(self):
        logging.info('DelTagFilter.run')
        while True :
            self.__data = self.__sourcePipe.get() # read data

            if isinstance( self.__data, TERMINATE ) :
                if STATE_ENUM.FIND_STARTTAG != self.__state :
                    error.errDesc = "TAG NOT MATCH"
                    error.errCode = ERROR_CODE.TAG_NOT_MATCH
                    logging.error("---Tag Not match---")
                self.__sinkPipe.put(self.__data)
                logging.info('DelTagFilter:run finish job')
                return          #finish job

            logging.debug('DelTagFilter:run  inputData '+ self.__data)
            self.__startPos = 0                   # not find
            self.__curTag = None
            self.__process()                           # process data

            logging.debug('DelTagFilter:run  SendData '+ self.__data)

            temp = self.__data.strip()
            if '' != temp :                             #skip empty line
                self.__sinkPipe.put(self.__data)       # send data

    def __process(self):
        while True :
            if STATE_ENUM.FIND_STARTTAG == self.__state :
                
                findPos = -1 # not found
                
                for startTag in self.__tagList:
                    pos = self.__data.find( startTag, self.__startPos )
                    
                    if -1 != pos :  # find
                        if -1 == findPos:      #first find
                            findPos = pos
                            self.__curTag = startTag
                        else:
                            if findPos > pos:
                                findPos = pos
                                self.__curTag = startTag

                if -1 == findPos :
                    return              # if not found nothing to do
                else:
                    self.__startPos = findPos
                    self.__state = STATE_ENUM.FIND_ENDTAG
                    continue
            elif STATE_ENUM.FIND_ENDTAG == self.__state:

                endPos = -1 #not found

                if None != self.__curTag :
                    findPos = self.__startPos + len(self.__curTag)
                else:
                    findPos = self.__startPos

                endPos = self.__data.find( self.__endTag , findPos )

                if -1 != endPos : # find
                    self.__data = self.__data[:self.__startPos] + self.__data[ (endPos+1 ):]
                    self.__startPos = 0
                    self.__state = STATE_ENUM.FIND_STARTTAG
                    continue        #re find
                else :              # not found
                    self.__data = self.__data[:self.__startPos]
                    return          # read next data
                    
            
