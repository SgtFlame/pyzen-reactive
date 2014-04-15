

class Aggregate(object):
    ''' Reactive Aggregate object 
    
    This is an aggregate of reactive elements.  Reactive elements can be queried
    for values but they cannot be directly modified.
    
    This object is mutable only through commands (lower camel case by 
    convention).
    '''
    def __init__(self, reactive):
        ''' Initialize the Aggregate
        
        Params
        ------
        reactive - AppManager
            Reactive app manager (used to gain access to the rest of the 
            reactive system)
        '''
        self._reactive = reactive
