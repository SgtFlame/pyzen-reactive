
#TODO Move elsewhere
def reactive_func(func):
    print('Applying reactive_func decorator')
    def _new_func(self, *args, **kwargs):
        
        func(self, *args, **kwargs)
    
    return _new_func

from client import ReactiveClient, AppManager
