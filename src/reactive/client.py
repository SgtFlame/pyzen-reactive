
from reactive.db_server.proxy import ReactiveServerProxy

def open_db(db_name, container):
    return ReactiveServerProxy(container)

class AppManager(object):

    def __init__(self, srap, db_stack):
        self._container = ServiceContainer()
        self._conmtainer.init(srap=srap)
        self._db = reactive.open_db(db_stack, self._container)

    @property
    def container(self):
        return self._container
        
    @property
    def db(self):
        return self._db

    def shutdown(self):
        self.db.disconnect()
        self.container.shutdown()
        
    def run(self):
        self.container.run()

    def call_later(self, seconds, task):
        self.container.call_later(seconds, task)
        