import datetime , string , psutil ,secrets , os ,ping3 , time


def getRandomKey(n=10,numbers=True) :
    if numbers :
        return ''.join(secrets.choice(string.ascii_lowercase + string.digits)
            for i in range(n))
    else :
        return ''.join(secrets.choice(string.ascii_lowercase )
            for i in range(n))


def now() :
    return datetime.datetime.now()

def date_time_now() :
    return  str( now().replace(microsecond=0))


def timenow() : 
    return  str(now().strftime("%d/%m/%Y %H:%M:%S"))
    

def timenowForLabels() : 
    return now().strftime("%d-%m-%Y_%H-%M-%S")


def getDateTimeAfterFewSeconds(seconds=10):
    import datetime
    # Get the current time
    current_time = datetime.datetime.now()
    # Add the specified number of seconds
    new_time = current_time + datetime.timedelta(seconds=seconds)
    # Format the new time as a string
    return new_time.strftime('%Y-%m-%d %H:%M')


def isOsPortFree(port : str):
    for conn in psutil.net_connections():
        if str(conn.laddr.port) == port :
            return False
    return True


def pingAddress( address ) : 
    response  = ping3.ping(f'{pingAddress}')
    if response == None :
        return False
    else :
        return True
