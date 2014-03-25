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
def create_app(self):
    
    user_class = meta.Class('user')
    # Properties are always private
    user_id = meta.property('user_id', 'string', 'Unique identifier for this user')
    login = meta.property('login', 'string', 'Login used by user')
    encrypted_password = meta.property('encrypted_password', 'string', 'Encrypted password to authenticate login')
    users = meta.collection('users', user_class)

    event_args = [ login, encrypted_password ]
    
    # Construct the meta process for handling this event
    # This is kinda Lua-ish
    event_process = [
        # Push a new user onto the stack
        meta.create('user'),
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

    user_class.event_handler('create', 'user_created', event_args, event_process)

    client_class = meta.Class('client')
    clients = meta.create_collection('clients', client_class)

    
    clients = meta.Collection()

    # Create a new user
    deferred = app_manager.db.execute('user create: login="{0}", encrypted_password="{1}"'.format(
            'TestUser@anonymous.com', encrypt('test password')))

    

app_manager.call_later(10, create_app)

app_manager.run()
