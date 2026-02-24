
import asyncio
from typing import Callable ,Any ,Optional
from functools import wraps
from pyrogram .errors import UnknownError ,FloodWait
from ntgcalls import TelegramServerError
from ..logging import LOGGER

class ErrorHandler :

    @staticmethod
    async def handle_tg_server_error (error :Exception ,operation :str ="operation",max_retries :int =3 )->bool :

        if isinstance (error ,FloodWait ):
            wait_time =error .value
            LOGGER (__name__ ).warning (f"FloodWait for {operation }: waiting {wait_time }s")
            await asyncio .sleep (wait_time )
            return True

        if isinstance (error ,TelegramServerError ):
            LOGGER (__name__ ).error (f"TelegramServerError in {operation }: {error }")

            await asyncio .sleep (2 )
            return True

        if isinstance (error ,UnknownError ):
            LOGGER (__name__ ).error (f"UnknownError in {operation }: {error }")

            await asyncio .sleep (5 )
            return True

        return False

    @staticmethod
    def retry_on_error (max_retries :int =3 ,backoff_factor :float =1.5 ,
    exceptions :tuple =(Exception ,)):

        def decorator (func :Callable )->Callable :
            @wraps (func )
            async def wrapper (*args :Any ,**kwargs :Any )->Any :
                last_error =None
                wait_time =1

                for attempt in range (max_retries ):
                    try :
                        return await func (*args ,**kwargs )
                    except exceptions as e :
                        last_error =e
                        if attempt <max_retries -1 :
                            LOGGER (__name__ ).warning (
                            f"{func .__name__ } failed (attempt {attempt +1 }/{max_retries }): {type (e ).__name__ }. "
                            f"Retrying in {wait_time }s..."
                            )
                            await asyncio .sleep (wait_time )
                            wait_time *=backoff_factor
                        else :
                            LOGGER (__name__ ).error (
                            f"{func .__name__ } failed after {max_retries } attempts: {e }"
                            )

                raise last_error

            return wrapper
        return decorator

def handle_unknown_constructor (error_msg :str )->Optional [str ]:

    if "unknown constructor"in str (error_msg ).lower ():
        return (
        "Unknown TL constructor detected. This usually means:\n"
        "1. Pyrogram schema is outdated\n"
        "2. Session file is corrupted\n"
        "3. API protocol mismatch\n"
        "Attempting automatic recovery..."
        )
    return None

async def safe_coroutine (coro ,timeout :int =30 ,default :Any =None )->Any :

    try :
        return await asyncio .wait_for (coro ,timeout =timeout )
    except asyncio .TimeoutError :
        LOGGER (__name__ ).warning (f"Coroutine timed out after {timeout }s, using default")
        return default
    except Exception as e :
        LOGGER (__name__ ).error (f"Coroutine failed: {e }")
        return default