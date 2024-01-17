from easy_utils_dev.custom_env import custom_env , enject_osenv
from time import sleep
from threading import Thread

enject_osenv()
env = custom_env()

def test() :
    while True :
        for key , value in env :
            print( f"{key} {value}" )
        sleep( 1 )

th = Thread( target=test )
th.daemon = True
th.start()