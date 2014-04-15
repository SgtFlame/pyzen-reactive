from zen.fabric.service_container import ServiceContainer

from reactive.data.proxy import CollectionProxy
from reactive.server.proxy import ReactiveServerProxy
from reactive.meta.proxy import MetaProxy

class ReactiveClient(object):

    def __init__(self, stack_name, app_manager):
        print('Initializing ReactiveClient')
        self._initialized = False
        self._app_manager = app_manager
        # Proxy for the reactive server
        self._server = ReactiveServerProxy(stack_name, app_manager.container)
        # Meta
        self._meta = MetaProxy(stack_name, app_manager.container)
        # Resolved attributes, generally service, collection, or object proxies
        self._resolved_attrs = {}
        print('ReactiveClient initialized')

    @property
    def app_manager(self):
        return self._app_manager

    @property
    def meta(self):
        print('Getting meta')
        meta = self._meta
        print('Got meta')
        return meta

    def disconnect(self):
        pass

    def install_hacks(self, hacks):
        ''' Install hacks to temporarily replace unimplemented portions
        of Reactive
        '''
        for key, value in hacks.iteritems():
            self._resolved_attrs[key] = value(self.app_manager)

    def __getattr__(self, name):
        if not self._initialized:
            raise RuntimeError()
        if name in self._resolved_attrs:
            return self._resolved_attrs[name]
        else:
            # For now assume that the top level attribute is the name of a collection
            collection = CollectionProxy(self, name)
            self._resolved_attrs[name] = collection
            return collection

class AppManager(object):

    def __init__(self, srap, stack_name):
        self._container = ServiceContainer()
        self._container.init(srap=srap)
        self._reactive = ReactiveClient(stack_name, self)

    @property
    def container(self):
        return self._container

    @property
    def reactive(self):
        print('Calling AppManager property reactive')
        return self._reactive

    def shutdown(self):
        self.db.disconnect()
        self.container.shutdown()
        
    def run(self):
        self.container.run()

    def call_later(self, seconds, task):
        self.container.call_later(seconds, task)
