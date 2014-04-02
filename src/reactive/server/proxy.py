from zen.fabric.service_proxy import ServiceProxy

class ReactiveServerProxy(ServiceProxy):

    def __init__(self, stack_name, container):
        super(ReactiveServerProxy, self).__init__(container)
