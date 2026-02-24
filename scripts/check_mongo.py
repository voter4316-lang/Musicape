
from os import getenv
import sys
from pymongo import MongoClient
from pymongo .errors import OperationFailure ,ServerSelectionTimeoutError

def get_mongo_uri ():

    if getenv ('MONGO_DB_URI'):
        return getenv ('MONGO_DB_URI'),'MONGO_DB_URI'

    if getenv ('MONGO_URL'):
        return getenv ('MONGO_URL'),'MONGO_URL'

    mongo_user =getenv ('MONGOUSER',getenv ('MONGO_INITDB_ROOT_USERNAME'))
    mongo_pass =getenv ('MONGOPASSWORD',getenv ('MONGO_INITDB_ROOT_PASSWORD'))
    mongo_host =getenv ('MONGOHOST',getenv ('RAILWAY_PRIVATE_DOMAIN'))
    mongo_port =getenv ('MONGOPORT','27017')

    if mongo_host :
        if mongo_pass :
            uri =f"mongodb://{mongo_user or 'mongo'}:{mongo_pass }@{mongo_host }:{mongo_port }/armedmusic?authSource=admin"
        else :
            uri =f"mongodb://{mongo_host }:{mongo_port }/armedmusic"
        return uri ,'CONSTRUCTED'

    return None ,None

mongo_uri ,source =get_mongo_uri ()

if not mongo_uri :
    print ('ERROR: Could not construct MONGO_DB_URI.')
    print ('Set either:')
    print ('  - MONGO_DB_URI environment variable, or')
    print ('  - MONGO_URL environment variable, or')
    print ('  - Individual components: MONGOUSER, MONGOPASSWORD, MONGOHOST, MONGOPORT')
    sys .exit (2 )

print (f'Testing MongoDB connection...')
print (f'Source: {source }')
print (f'URI: {mongo_uri [:80 ]}...'if len (mongo_uri )>80 else f'URI: {mongo_uri }')

try :
    client =MongoClient (mongo_uri ,serverSelectionTimeoutMS =10000 ,connectTimeoutMS =10000 )
    client .admin .command ('ping')
    print ('✓ Ping succeeded.')

    dbs =client .list_database_names ()
    print (f'✓ Authentication successful. Found {len (dbs )} database(s).')
    print ('✓ Connection OK')
    sys .exit (0 )

except OperationFailure as e :
    print ('✗ Authentication failed. Please verify:')
    print ('  - Username and password are correct')
    print ('  - authSource parameter is set (usually "admin")')
    print ('  - User exists in the admin database')
    print (f'Error: {e }')
    sys .exit (3 )

except ServerSelectionTimeoutError as e :
    print ('✗ Server selection/connection timed out. Please verify:')
    print ('  - MongoDB host is reachable and online')
    print ('  - Host address is correct')
    print ('  - Port is correct (default 27017)')
    print ('  - Network connectivity is available')
    print (f'Error: {e }')
    sys .exit (4 )

except Exception as e :
    print (f'✗ Unexpected error while connecting to MongoDB: {type (e ).__name__ }')
    print (f'Error: {e }')
    sys .exit (1 )