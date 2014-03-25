

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

stack = 'test'

db_name = '{0}-db'.format(stack)

client.drop_database(db_name)
db = client[db_name]

print('Collections before starting: {0}'.format(db.collection_names()))

collection = db['{0}-meta'.format(stack)]

doc = { 'test' : 1 }

collection.save(doc)

print('Collections afer test: {0}'.format(db.collection_names()))
