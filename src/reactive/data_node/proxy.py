from zen.fabric.service_proxy import ServiceProxy

class DataNodeProxy(ServiceProxy):

    def __init__(self, stack_name, container):
        super(DataNodeProxy, self).__init__(container)
