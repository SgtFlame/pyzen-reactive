from zen.fabric.batch_service_container import BatchServiceContainer
from zen.fabric.service import Service

from reactive.data_registry.proxy import DataRegistryProxy

class DataNode(Service):
    ''' Data Node '''

    def __init__(self, stack_name, container):
        super(DataNode, self).__init__(container)
        self._stack_name = stack_name
        self._data_registry = DataRegistryProxy(stack_name, container)

    def register(self, args):
        ''' Register with the DataRegistry / ServiceRegistry '''
        self._data_registry.register(self)

# Main function that run this service in a standalone process
def main():
    import argparse
    # Get arguments
    arg_parser = argparse.ArgumentParser(description='Run a Data Node')
    arg_parser.add_argument('--srap', default='localhost:8888', help='Service Registry address:port')
    arg_parser.add_argument('--stack', default='test', help='Reactive DB stack')

    args = arg_parser.parse_args()

    # Run Main
    # Create service container and service(s)
    container = BatchServiceContainer()
    container.init(srap=args.srap)

    data_node = DataNode(args.stack, container)

    # The service registry is always only a local service because it shouldn't 
    # be registered with another service registry (at least not until there are
    # redundant service registries)
    #TODO This registration is deferred until the data registry assigns a name to this node
    #container.register_service(data_registry, '/datagrid/{0}/registry'.format(args.stack))

    container.call_later(1, data_node.register)

    container.run()

if __name__ == "__main__":
    main()
