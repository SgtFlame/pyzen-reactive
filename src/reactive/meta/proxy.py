from zen.fabric.service_proxy import ServiceProxy
from reactive.data.proxy import CollectionProxy, ClassProxy
from reactive.api import reactive_func

class MetaProxy(ServiceProxy):

    def __init__(self, stack_name, app_manager):
        super(MetaProxy, self).__init__(app_manager.container)
        self._reactive = app_manager.reactive
        self._stack_name = stack_name
        self._classes = {}
        self._collections = {}

    @property
    def reactive(self):
        return self._reactive

    @property
    def path(self):
        return '/datagrid/{0}/meta'.format(self._stack_name)

    def createClass(self, class_name, language, implementation, update=True):
        ''' Create a class 
        Params
        ------
        class_name : string
            Name of the class to create
        language : string
            Language that the node supports; 
            one of ('python', 'java', 'c++', 'ruby', 'zlang', 'metazen', etc)
        implementation : string
            Location of the implementation (using language, this is the fully qualified
            name of the native class that handles the implementation of this meta
            class)
        update : boolean
            If True, update the class if the class already exists.  If False, only
            create the class.  If the class already exists and update=False then
            an error is raised
        Returns
        -------
        proxy_class : ClassProxy
            ClassProxy to stand-in for the class that is to be created (or was
            already created)
        '''
        if class_name in self._classes:
            return self._classes[class_name]
        request = {
            'command' : 'createClass',
            'path' : self.path,
            'args' : {  'class_name' : class_name, 
                        'language' : language, 
                        'implementation' : implementation,
                        'update' : update,
                    }
        }
        meta_responded = self.queue_request(request)
        proxy_class = ClassProxy(self.reactive, class_name, deferred=meta_responded)
        self._classes[class_name] = proxy_class
        return proxy_class

    @reactive_func
    def createCollection(self, contains, collection_name=None, distributed=True):
        ''' Create a collection of reactive objects

        Params
        ------
        contains : string
            Type of object that the collection contains
        collection_name : string, optional
            Name of the collection
        distributed : boolean
            True if this collection is distributed across multiple data nodes

        TODO Support affinity / other hints that indicate how and where to distribute
        the collection

        Returns
        -------
        collection : CollectionProxy
            Reference to the newly created collection; this probably should be
            a deferred / promise / future.
        '''
        
        if collection_name in self._collections:
            return self._collections[collection_name]
        request = {
            'command' : 'createCollection',
            'path' : self.path,
            'args' : {  'collection_name' : collection_name, 
                        'contains' : contains,
                        'distributed' : distributed, 
                    }
        }
        print('About to send {0}'.format(request))
        meta_responded = self.queue_request(request)
        print('Sent request, got {0} back, creating CollectionProxy'.format(meta_responded))
        proxy_collection = CollectionProxy(self.reactive, collection_name, deferred=meta_responded)
        self._collections[collection_name] = proxy_collection
        return proxy_collection

    def getCollection(self, collection_name):
        #TODO This should be deferred
        return self._collections[collection_name]
