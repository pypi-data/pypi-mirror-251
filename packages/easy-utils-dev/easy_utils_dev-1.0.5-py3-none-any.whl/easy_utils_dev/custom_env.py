import os 

'''
in custom env. you can setup custom environment and store any object. not like normal env...
which can store only strings.
'''


_custom_env= {}

def enject_osenv() :
    global _custom_env
    for key , value in os.environ.items():
        _custom_env[key] = value

def custom_env():
    return _custom_env






