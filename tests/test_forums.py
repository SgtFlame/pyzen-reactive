import argparse
from reactive import client as reactive

# Get arguments
arg_parser = argparse.ArgumentParser(description='Run the test client')
arg_parser.add_argument('--srap', help='Service Registry address:port')
arg_parser.add_argument('--stack', help='Reactive DB stack')

args = arg_parser.parse_args()

# Run Main
app_manager = reactive.AppManager(srap, 'test')

# Create the application
def create_app():

    user_class = meta.Class('User')
    # Properties are always private
    user_id = meta.Property('user_id', 'string', 'Unique identifier for this user')
    login = meta.Property('login', 'string', 'Login used by user')
    encrypted_password = meta.Property('encrypted_password', 'string', 
        'Encrypted password to authenticate login')

    user_class.properties += [user_id, login, encrypted_password]

    users = meta.Collection('Users', user_class)
    user_class.default_collection = users

    event_args = [login, encrypted_password]

    # Construct the meta process for handling this event
    # This is kinda Lua-ish
    event_process = [
        # Push a new user onto the stack
        meta.create('User'),
        #(or should it be like this?)
        #meta.create(-1) and have the top of the stack be the current class?
        # Generate the unique id of the user and push it onto the stack
        meta.generate_unique_id('user'),
        # Set the object (-2 on the stack) user_id property using top of stack
        meta.set_property(-2, 'user_id', meta.value(-1)),
        # set the object login property using the login argument
        meta.set_property(-2, 'login', login),
        meta.set_property(-2, 'encrypted_password', encrypted_password),
        # Everything on the stack is returned, which means -1 (user_id) 
        # and -2 (user object)
    ]

    # user_created event, created by User.create()
    user_class.class_event_handler('create', 'user_created', event_args, event_process)

    client_class = meta.Class('Client')
    clients = meta.Collection('Clients', client_class)

    # client_connected event, created by Client.connect(ip_address, 

    # Create a new user
    deferred = app_manager.db.User.create(login='TestUser@anonymous.com', encrypted_password=encrypt('Test password'))

    #TODO Instead of a deferred, we should create something else that
    # can support a timeout; I suppose for now we can use an errBack for timeouts.
    deferred.addCallback(user_created)

    # Here's where the procedural meets reactive
    

def user_created(args):
    user_id = args[0]
    user = args[1]



app_manager.call_later(10, create_app)

app_manager.run()
