from twisted.internet import defer

from zen.fabric.service_proxy import ServiceProxy

class DataRegistryProxy(ServiceProxy):

    def __init__(self, stack_name, container):
        super(DataRegistryProxy, self).__init__(container)
        self._stack_name = stack_name
        
    @property
    def path(self):
        #TODO move path const to module?  This is formatted twice, once in 
        # service and once here in proxy.
        return '/datagrid/{0}/registry'.format(self._stack_name)

    def _service_registered(self, msg, readied):
        ''' Called when the service has been registered with the service
        registry
        '''
        #TODO double-check the msg to make sure of success?
        print('Registered with service registry.')
        readied.callback(None)

    def _node_registered(self, response, readied):
        ''' Called when the DataNode has been registered with the DataRegistry 
        '''
        print('Registered with data registry, response was {0}'.format(response))
        self._node_name = response['node_name']
        service_registered = self._container.register_service(self, '/datagrid/{0}/{1}'.format(self._stack_name, self._node_name))
        service_registered.addCallback(self._service_registered, readied)

    def register(self, data_node):
        ''' Register a data node with the DataRegistry

        Params
        ------
        data_node : DataNode
            DataNode that needs to be registered
        '''
        request = {
            'command' : 'register',
            'path' : self.path,
            'args' : { 'language' : 'python' },
        }
        registered = self._container.send_request(request)
        readied = defer.Deferred()
        registered.addCallback(self._node_registered, readied)

        return readied

    