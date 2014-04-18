from zen.fabric.service_container import ServiceContainer

from reactive.data.proxy import CollectionProxy
from reactive.server.proxy import ReactiveServerProxy
from reactive.meta.proxy import MetaProxy

class ReactiveClient(object):

    def __init__(self, stack_name, app_manager):
        self._initialized = False
        self._stack_name = stack_name
        self._app_manager = app_manager
        
    def init(self):
        ''' Additional initialization '''
        # Proxy for the reactive server
        self._server = ReactiveServerProxy(self._stack_name, self._app_manager.container)
        # Meta
        self._meta = MetaProxy(self._stack_name, self._app_manager)
        # Resolved attributes, generally service, collection, or object proxies
        self._resolved_attrs = {}
        self._initialized = True

    @property
    def app_manager(self):
        return self._app_manager

    @property
    def meta(self):
        meta = self._meta
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
        self._reactive.init()

    @property
    def container(self):
        return self._container

    @property
    def reactive(self):
        return self._reactive

    def shutdown(self):
        self.db.disconnect()
        self.container.shutdown()
        
    def run(self):
        self.container.run()

    def call_later(self, seconds, task):
        self.container.call_later(seconds, task)
