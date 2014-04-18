import pymongo
import bson.json_util

from zen.fabric.batch_service_container import BatchServiceContainer
from zen.fabric.service import Service

class ClassMeta(object):
    
    def __init__(self, doc=None):
        self._doc = doc

    def get_doc(self):
        pass

    def serialize(self):
        return { 'class_name' : doc['class_name'],
            'language' : doc['language'],
            'implementation' : doc['implementation']
        }

class MetaService(Service):
    ''' Data Registry '''

    def __init__(self, stack):
        #TODO it's bad form to directly use MongoDB instead of using
        # another generic interface, but I'm going to do it for 
        # simplicty / expediency
        self._stack = stack
        self._mongo_client = client = pymongo.MongoClient('mongodb://localhost:27017')
        db_name = '{0}-db'.format(stack)
        self._db = client[db_name]
        # Meta database collection (cached meta data)
        self._meta = self._db['{0}-meta'.format(stack)]
        # Meta events (use these events to reconstruct the meta data)
        self._meta_events = self._db['{0}-meta-events'.format(stack)]
        self._classes = {}
        self._collections = {}
        collections = self._meta.find({'type' : 'collection'})
        for collection in collections:
            self._collections[collection['name']] = collection
        classes = self._meta.find({'type' : 'class'})
        for class_data in classes:
            print('Class: {0}, type({1})'.format(class_data, type(class_data)))
            self._classes[class_data['name']] = class_data
    
    def createClass(self, class_name, language, implementation, update):
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
        '''
        if class_name not in self._classes:
            print('Creating class {0}'.format(class_name))
            self._create_class(class_name, language, implementation)
        class_data = self._classes[class_name]
        print('Class: {0}, type({1})'.format(class_data, type(class_data)))
        return class_data
    
    def createCollection(self, contains, collection_name, distributed):
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
        collection_data : dict
            Mongo document representing the collection meta data (probably
            should be something else, but needs to be JSON serializable)
        '''
        if collection_name not in self._collections:
            print('Creating collection {0}'.format(collection_name))
            self._create_collection(contains, collection_name, distributed)
        collection_data = self._collections[collection_name]
        return collection_data

    def _create_class(self, class_name, language, implementation):
        class_data = {
            'name' : class_name,
            'language' : language,
            'implementation' : implementation,
        }
        meta_event = {
            'type' : 'class_created',
            'data' : class_data,
        }
        #TODO This MetaService probably should also be an Aggregate
        # and at this point the meta_event should be passed to the aggregate
        # handler, but since that's not implemented yet then the event is
        # handled here.
        #self._handle_event(event)
        self._classes[class_name] = class_data
        self._meta_events.save(meta_event)
        #TODO Syncronize the Aggregate (This saves the aggregate to the
        # cache and indicates the events that have been applied, but since
        # that's not implemented yet then handle the implementation inline here
        #self.synchronize()
        self._meta.save(class_data)
        print('Class: {0}, type({1})'.format(class_data, type(class_data)))
        #TODO This event should be published to listeners
        return meta_event

    def _create_collection(self, contains, collection_name, distributed):
        #TODO The same things that need to be done for classes should be done
        # for collections as well.
        collection_data = {
            'contains' : contains,
            'collection_name' : collection_name,
            'distributed' : distributed,
        }
        meta_event = {
            'type' : 'collection_created',
            'data' : collection_data,
        }
        self._collections[collection_name] = collection_data
        self._meta_events.save(meta_event)
        self._meta.save(collection_data)
        return meta_event

# Main function that run this service in a standalone process
def main():
    import argparse
    # Get arguments
    arg_parser = argparse.ArgumentParser(description='Run the Meta Service')
    arg_parser.add_argument('--srap', default='localhost:8888', help='Service Registry address:port')
    arg_parser.add_argument('--stack', default='test', help='Reactive DB stack')

    args = arg_parser.parse_args()

    # Run Main
    # Create service container and service(s)
    container = BatchServiceContainer(bson.json_util.default)
    container.init(srap=args.srap)

    meta_service = MetaService(args.stack)
    
    # The service registry is always only a local service because it shouldn't 
    # be registered with another service registry (at least not until there are
    # redundant service registries)
    container.register_service(meta_service, '/datagrid/{0}/meta'.format(args.stack))

    container.run()

if __name__ == "__main__":
    main()
    