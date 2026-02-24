import sys
import os

def check_python_version ():

    print ("Checking Python version...",end =" ")
    if sys .version_info <(3 ,8 ):
        print (f"✗ (requires 3.8+, got {sys .version_info .major }.{sys .version_info .minor })")
        return False
    print (f"✓ ({sys .version_info .major }.{sys .version_info .minor }.{sys .version_info .micro })")
    return True

def check_dependencies ():

    print ("\nChecking dependencies...")
    required_packages ={
    'pyrogram':'Pyrogram',
    'pytgcalls':'PyTgCalls',
    'motor':'Motor',
    'aiohttp':'aiohttp',
    'pymongo':'PyMongo',
    'yt_dlp':'yt-dlp',
    }

    all_ok =True
    for module ,name in required_packages .items ():
        try :
            __import__ (module )
            print (f"  ✓ {name }")
        except ImportError :
            print (f"  ✗ {name } NOT INSTALLED")
            all_ok =False

    return all_ok

def check_environment_variables ():

    print ("\nChecking environment variables...")
    required_vars ={
    'API_ID':'Telegram API ID',
    'API_HASH':'Telegram API Hash',
    'BOT_TOKEN':'Telegram Bot Token',
    'LOGGER_ID':'Logger Group/Channel ID',
    'PREFIX':'Bot Command Prefix',
    }

    all_ok =True
    for var ,description in required_vars .items ():
        if os .getenv (var ):
            print (f"  ✓ {var }")
        else :
            print (f"  ✗ {var } - NOT SET ({description })")
            all_ok =False

    return all_ok

def check_session_files ():

    print ("\nChecking session files...")
    session_files =[
    'session.session',
    ]

    all_ok =True
    for filename in session_files :
        if os .path .exists (filename ):
            size =os .path .getsize (filename )
            print (f"  ✓ {filename } ({size } bytes)")
        else :
            print (f"  ⚠ {filename } - NOT FOUND (will be created on first run)")

    return True

def check_directories ():

    print ("\nChecking directories...")
    required_dirs =[
    'Music',
    'Music/core',
    'Music/plugins',
    'Music/utils',
    'strings',
    ]

    all_ok =True
    for dirname in required_dirs :
        if os .path .isdir (dirname ):
            print (f"  ✓ {dirname }")
        else :
            print (f"  ✗ {dirname } - NOT FOUND")
            all_ok =False

    return all_ok

def check_config ():

    print ("\nChecking configuration...")
    try :
        import config
        print (f"  ✓ config.py loaded")
        return True
    except Exception as e :
        print (f"  ✗ config.py error: {e }")
        return False

def main ():

    print ("\n"+"="*50 )
    print ("🎵 Music Bot - Health Check")
    print ("="*50 +"\n")

    checks =[
    ("Python Version",check_python_version ),
    ("Dependencies",check_dependencies ),
    ("Environment Variables",check_environment_variables ),
    ("Directories",check_directories ),
    ("Configuration",check_config ),
    ("Session Files",check_session_files ),
    ]

    results =[]
    for name ,check_func in checks :
        try :
            result =check_func ()
            results .append ((name ,result ))
        except Exception as e :
            print (f"Error during {name } check: {e }")
            results .append ((name ,False ))

    print ("\n"+"="*50 )
    print ("Summary:")
    print ("="*50 )

    passed =sum (1 for _ ,result in results if result )
    total =len (results )

    for name ,result in results :
        status ="✓ PASS"if result else "✗ FAIL"
        print (f"  {status }: {name }")

    print (f"\nResult: {passed }/{total } checks passed")

    if passed ==total :
        print ("\n✅ All checks passed! Bot is ready to start.")
        print ("\nTo start the bot, run:")
        print ("  python -m Music")
        return 0
    else :
        print ("\n❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ =='__main__':
    sys .exit (main ())