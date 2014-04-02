
from reactive.server.proxy import ReactiveServerProxy

class ReactiveClient(object):
    
    def __init__(self, stack_name, app_manager):
        self._app_manager = app_manager
        # Proxy for the reactive server
        self._server = ReactiveServerProxy(stack_name, app_manager.container)
        # Resolved attributes, generally service, collection, or object proxies
        self._resolved_attrs = {}

    @property
    def app_manager(self):
        return self._app_manager

    def disconnect(self):
        pass

    def install_hacks(self, hacks):
        ''' Install hacks to temporarily replace unimplemented portions
        of Reactive
        '''
        for key, value in hacks.iteritems():
            self._resolved_attrs[key] = value(self.app_manager)

    def __getattr__(self, name):
        if name in self._resolved_attrs:
            return self._resolved_attrs[name]
        else:
            raise RuntimeError('Reactive meta not found for {0}'.format(name))


class AppManager(object):

    def __init__(self, srap, stack_name):
        self._container = ServiceContainer()
        self._container.init(srap=srap)
        self._reactive = ReactiveClient(stack_name, self._container)

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
