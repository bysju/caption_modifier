
class _const:
    def __init__(self):
        self.__dict__ = {}
    class ConstError(TypeError): pass
    def __setattr__(self, name, value):
#        if self.__dict__.has_key(name):
#        print name in self.__dict__
        if name in self.__dict__ :
            raise self.ConstError( "Can't rebind const(%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__] = _const()
