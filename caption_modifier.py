import const, Filters, queue, sys

class BadIniFile(Exception):
    pass

const.SOURCE = "source"
const.SINK = "sink"
const.PIPE = "pipe"
const.FILTERS = "filters"

const.SEP_KEY_VALUE = ":"
const.SEP_VALUE = ","
const.SEP_ARGUMENT = "|"


class Factory:
    def __init__(self, iniFile):  #load iniFile
        __load(iniFile)
        self.__dic = {}
        self.__pipeList = []
        self.__filterList = []

    def __load(self, iniFile):
        file = open(iniFile)
        #make dictionary
        for line in file.readlines():
            __innerLoad(line)


    def __innerLoad(self, line):

        keyValueList  = line.split( const.SEP_KEY_VALUE )

        if 2 != len(keyValueList) :  # must conist key : value
            raise BadIniFile("Invalid key value IniFile (%s)" % line )

        if const.FILTERS == keyValueList[0] :  # filters is plural
            self.__dic[keyValueList[0] ] = keyValueList[1]
            #self.__dic[keyValueList[0] ] = keyValueList[1].split( const.SEP_VALUE )
           

        else:
            if 1 != len( keyValueList[1].split( const.SEP_VALUE ) ) :
                raise BadIniFile( "Too many value IniFile (%s)"% line)
            self.__dic[keyValueList[0] ] = keyValueList[1]

    def create(self, sourceFile, destFile):
        """ make queue and soruceFilter"""
        queueSrc = __makeClass( self.__dic[const.PIPE] )
        argList = []
        argList.append(queueSrc)
        argList.append(sourceFile)
        
        srcFilter = __makeClass( self.__dic[const.SOURCE], argList ) 

        self.__pipeList.append( queueSrc)
        self.__filterList.append( srcFilter)
                
        """ make Filters """
        sourcePipe = queueSrc
        for filterExp in self.__dic[const.FILTERS].split( const.SEP_VALUE ) :
            queue = __makeClass( self.__dic[const.PIPE] )
                                 
            sinkPipe = queue
            argList = []
            argList.append( sourcePipe)
            argList.append( sinkPipe)
               
            centerFilter =  __makeClass( filterExp , argList)
            self.__pipeList.append(queue)
            self.__filterList.append(centerFilter)
            sourcePipe = queue

        """ make SinkFilter """
        argList = []
        argList.append( sinkPipe)
        argList.append( destFile)
        sinkFilter = __makeClass( self.__dic[const.SINK], argList ) 
        self.__filterList.append(sinkFilter)

    def __makeClass( self, expression, preArgList = None ):
        """ make preArgument """
        expList = expression.split( const.SEP_ARGUMENT )

        if 2 != len(expList) :
            raise BadIniFile( "Invalid class expression (%s)"% expression)

        strExp = expList[0] + "("

        """ add preArgList """
        if None != preArgList :
            for i in range(preArgList) :
                strExp += "preArgList[" + i + "],"

        """ add argument """
        strExp += expList[1] + ")"

        return eval( strExp )

    def run(self):
        """ start run method in thread """

        for thread in self.__filterList :
            thread.start()

        for thread in self.__filterList :
            thread.join()                   # wait for thread exits



def main():
    if 3 == len(sys.argv) or 4 == len(sys.argv) :
        sourceFile = sys.argv[1]
        sinkFile = sys.argv[2]
        if 4 == len(sys.argv) :
            iniFile = sys.argv[3]
        else:
            iniFile = "./default.ini"

        # create Factory
        factory = Factory(iniFile)

        factory.create( sourceFile, sinkFile)

        factory.run()

        #finish
    else:
        print ("usage : [sourceFile] [destFile] [iniFile]")

        
if __name__ == "__main__":
    main()
                          
                          
                          
                          
        
        
        
        

        
            

        
        
        
        
        
