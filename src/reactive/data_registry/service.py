from zen.fabric.batch_service_container import BatchServiceContainer
from zen.fabric.service import Service

from reactive.data_node.proxy import DataNodeProxy

class DataRegistry(Service):
    ''' Data Registry '''

    def __init__(self, stack):
        self._stack = stack
        # All nodes indexed by node_name
        self._nodes = {}
        # Node names indexed by language
        self._language_index = {}

    def register(self, language):
        ''' Register a data node

        Params
        ------
        language : string
            Language that the node supports; 
            one of ('python', 'java', 'c++', 'ruby', 'zlang', 'metazen', etc)

        Returns
        -------
        node_name : string
            Name of the node service that should be registered with the service
            registry.
        '''
        node_index = len(self._nodes)
        node_name = 'node%04d' % (node_index)
        self._nodes[node_name] = DataNodeProxy(self._stack, self._container)
        if language not in self._language_index:
            self._language_index[language] = []
        self._language_index[language].append(node_name)
        return {'status': 'ok', 'node_name': node_name}

# Main function that run this service in a standalone process
def main():
    import argparse
    # Get arguments
    arg_parser = argparse.ArgumentParser(description='Run the Data Registry')
    arg_parser.add_argument('--srap', default='localhost:8888', help='Service Registry address:port')
    arg_parser.add_argument('--stack', default='test', help='Reactive DB stack')

    args = arg_parser.parse_args()

    # Run Main
    # Create service container and service(s)
    container = BatchServiceContainer()
    container.init(srap=args.srap)

    data_registry = DataRegistry(args.stack)

    # The service registry is always only a local service because it shouldn't 
    # be registered with another service registry (at least not until there are
    # redundant service registries)
    container.register_service(data_registry, '/datagrid/{0}/registry'.format(args.stack))

    container.run()

if __name__ == "__main__":
    main()
