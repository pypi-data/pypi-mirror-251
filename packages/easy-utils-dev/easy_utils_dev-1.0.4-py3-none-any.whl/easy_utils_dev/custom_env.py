import os 
from argparse import Namespace as _custom_env

'''
in custom env. you can setup custom environment and store any object. not like normal env...
which can store only strings.
'''


def enject_osenv() :
    for key , value in os.environ.items():
        _custom_env[key] = value

def custom_env():
    return _custom_env






