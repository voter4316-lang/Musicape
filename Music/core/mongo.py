from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from pymongo.errors import OperationFailure ,ServerSelectionTimeoutError
from config import MONGO_DB_URI ,MONGO_DB_NAME
from ..logging import LOGGER
import time

logger =LOGGER (__name__ )

def _connect_mongodb_with_retry (max_retries =3 ,initial_delay =2 ):

    logger .info ('Connecting to MongoDB database...')
    logger .info (f'Using database: {MONGO_DB_NAME }')

    for attempt in range (1 ,max_retries +1 ):
        try :
            logger .info (f'Connection attempt {attempt }/{max_retries }...')

            sync_client =MongoClient (MONGO_DB_URI ,serverSelectionTimeoutMS =10000 ,connectTimeoutMS =10000 )

            sync_client .admin .command ('ping')
            logger .info ('✓ MongoDB ping successful')

            dbs =sync_client .list_database_names ()
            logger .info (f'✓ Authentication successful. Found {len (dbs )} database(s)')

            sync_client .close ()

            async_client =AsyncIOMotorClient (
            MONGO_DB_URI ,
            serverSelectionTimeoutMS =10000 ,
            connectTimeoutMS =10000 ,
            retryWrites =True
            )

            mongodb =async_client [MONGO_DB_NAME ]
            logger .info ('✓ MongoDB async client created successfully')

            return mongodb

        except OperationFailure as auth_err :
            logger .error (f'MongoDB authentication failed: {auth_err }')
            if attempt <max_retries :
                wait_time =initial_delay *(2 **(attempt -1 ))
                logger .warning (f'Retrying in {wait_time }s...')
                time .sleep (wait_time )
            else :
                logger .error ('MongoDB authentication failed after all retries. Check MONGO_DB_URI and credentials.')
                raise

        except ServerSelectionTimeoutError as timeout_err :
            logger .error (f'MongoDB server selection timeout: {timeout_err }')
            if attempt <max_retries :
                wait_time =initial_delay *(2 **(attempt -1 ))
                logger .warning (f'Retrying in {wait_time }s...')
                time .sleep (wait_time )
            else :
                logger .error ('MongoDB connection timeout after all retries. Check host and network connectivity.')
                raise

        except Exception as e :
            logger .error (f'MongoDB connection error: {type (e ).__name__ }: {e }')
            if attempt <max_retries :
                wait_time =initial_delay *(2 **(attempt -1 ))
                logger .warning (f'Retrying in {wait_time }s...')
                time .sleep (wait_time )
            else :
                raise

try :
    mongodb =_connect_mongodb_with_retry (max_retries =3 ,initial_delay =2 )
    logger .info ('MongoDB connection initialized successfully')

except Exception as e :
    logger .critical (f'Failed to initialize MongoDB client: {e }')
    logger .critical ('Application cannot start without MongoDB connection')
    exit (1 )
