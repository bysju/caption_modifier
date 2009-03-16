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
            self.__sinkPipe.push(line)  #push file data

        self.__sinkPipe.push( queuePipe.TERMINATE)  #terminate job

class SinkFileFilter(pipesAndFilters.ThreadFilters):
    def __init__(self, sinkFile, sourcePipe  ):
        pipesAndFilters.ThreadFilters.__init__(sourcePipe, None)
        self.__file = open(sinkFile, 'w')
        assert(None != sourcePipe)
    def run(self):
        data = self.__sourcePipe.pull()
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

    def run(self):
        while True :
            self.__data = self.__sourcePipe.pull() # read data
            if isinstance( data, queuePipe.TERMINATE ) :
                if STATE_ENUM.FIND_STARTTAG != self.__state :
                    error.errDesc = "TAG NOT MATCH"
                    error.errCode = ERROR_CODE.TAG_NOT_MATCH
                self.__sinkPipe.push(self.__data)
                return          #finish job

            __process()                           # process data

            self.__sinkPipe.push(self.__data)       # send data

    def __process():
        while 
            
