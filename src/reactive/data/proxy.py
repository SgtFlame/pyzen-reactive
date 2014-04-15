from zen.fabric.service_proxy import ServiceProxy

class DataProxy(ServiceProxy):

    def create(self, collection_meta, **args):
        ''' Create a new object.
        
        Params
        ------
        collection_meta : ReactiveValue
            Meta data of the collection that will contain the newly created
            object.
        args : dictionary
            Additional arguments to be passed to the class constructor.
        '''
        raise RuntimeError('Not implemented')
        
    def find(self, collection_meta, new_collection_name=None, **args):
        ''' Find one or more objects in a collection using the specified 
        arguments.
        
        Params
        ------
        collection_meta : ReactiveValue
            Meta data of the collection that will contain the newly created
            object.
        new_collection_name : string
            Name of the new collection.
        args : dictionary
            Additional arguments to be passed to the class constructor.
        '''
        
class ProxyObject(object):
    def __init__(self, reactive):
        self._reactive = reactive
        self._name = collection_name

class CollectionProxy(ProxyObject):

    def __init__(self, reactive, collection_name, deferred=None):
        super(CollectionProxy, self).super(reactive)
        # Get the meta data for this collection
        self._meta = self._reactive.meta.getCollection(collection_name)
        if deferred:
            deferred.addCallback(self._collection_created)

    def create(self, **args):
        ''' Create an object using the collection's default type '''
        return self._reactive.data.create(self._meta, **args)

    def find(self, **args):
        ''' Find objects using the args as a query filter '''
        return self._reactive.data.find(self._meta, **args)

    def find_first(self, **args):
        ''' Find the first object that matches the query filter 
        specified by args.
        '''
        return self._reactive.data.find_first(self._meta, **args)

    def find_one(self, **args):
        ''' Find an object that matches the query filter specified by args.
        The query should return one and only one object, and if more than one
        object matches the filter then an error should be raised.
        '''
        return self._reactive.data.find_one(self._meta, **args)

    def _collection_created(self, response):
        # Not really anything to do here yet
        pass

class ClassProxy(ProxyObject):

    def __init__(self, reactive, class_name, deferred=None):
        super(ClassProxy, self).super(reactive)
        self._class_name = class_name
        if deferred:
            deferred.addCallback(self._class_created)
        
    def _class_created(self, response):
        # Not really anything to do here yet
        pass
        