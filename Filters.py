import pipesAndFilters, queuePipe

error = pipesAndFilters.Error()

class STATE_ENUM:
    FIND_STARTTAG = 0
    FIND_ENDTAG = 1

class ERORR_CODE:
    TAG_NOT_MATCH = 0

class SrcFileFilter(pipesAndFilters.ThreadFilters):
    def __init__(self, sourceFile,  sinkPipe ):
        pipesAndFilters.ThreadFilters.__init__(None, sinkPipe)
        self.__file = open(sourceFile)
        assert(None != sinkPipe)
    def run(self):      # run provieds thread logic
        #read file
        lines = self.__fine.readlines()
        for line in lines:
            self.__sinkPipe.put(line)  #push file data

        self.__sinkPipe.put( queuePipe.TERMINATE)  #terminate job

class SinkFileFilter(pipesAndFilters.ThreadFilters):
    def __init__(self, sinkFile, sourcePipe  ):
        pipesAndFilters.ThreadFilters.__init__(sourcePipe, None)
        self.__file = open(sinkFile, 'w')
        assert(None != sourcePipe)
    def run(self):
        data = self.__sourcePipe.get()
        if isinstance( data, queuePipe.TERMINATE ) :
            return      #finish job

        self.__file.write(data)


class DelTagFilter(pipesAndFilters.ThreadFilters):
    def __init__(self, tagList, sourcePipe, sinkPipe,  ):
        pipesAndFilters.ThreadFilters.__init(sourcePipe, sinkPipe)
        self.__tagList = tagList
        assert(None != sourcePipe)
        assert(None != sinkPipe)
        self.__endTag = '>'
        self.__state = STATE_ENUM.FIND_STARTTAG
        self.__startTagPosition  = 0                # location of start tag
        self.__endTagPosition    = 0               # location of end tag

    def run(self):
        while True :
            self.__data = self.__sourcePipe.get() # read data
            if isinstance( data, queuePipe.TERMINATE ) :
                if STATE_ENUM.FIND_STARTTAG != self.__state :
                    error.errDesc = "TAG NOT MATCH"
                    error.errCode = ERROR_CODE.TAG_NOT_MATCH
                self.__sinkPipe.put(self.__data)
                return          #finish job

            self.__startPos = 0                   # not find
            self.__curTag = None
            __process()                           # process data

            self.__sinkPipe.put(self.__data)       # send data

    def __process():
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
                    self.__data = self.__data[:self.__startPos] + self.__data[endPos:]
                    self.__startPos = 0
                    self.__state = STATE_ENUM.FIND_STARTTAG
                    continue        #re find
                else :              # not found
                    self.__data = self.__data[:self.__startPos]
                    return          # read next data
                    
            
