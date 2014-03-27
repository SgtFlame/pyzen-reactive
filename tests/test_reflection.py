

class DeferredImplementation(object):
    def __init__(self, parent=None, name=None):
        self._parent = parent
        self._name = name
        self._child = None

    def __getattribute__(self, name):
        if hasattr(self, name):
            return super(DeferredImplementation, self).__getattribute__(name)
        else:
            self._child = DeferredImplementation(self, name)
            return self._child
            
    def __call__(self, *args, **kwargs):
        print('Calling {0} from {1} with args {2} and {3}'.format(self._name, 
            self._parent._name, args, kwargs))
            
db = DeferredImplementation()
db.User.create(arg1=1, arg2=2)
