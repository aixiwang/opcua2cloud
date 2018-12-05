import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server
from opcua.server.history_sql import HistorySQLite

import redis

HOST = '180.76.242.57'
KEY = 'xxx'

if __name__ == "__main__":
    r = redis.Redis(host=HOST, port=6379, db=0)

    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "MyObject")

    len = r.llen(KEY)
    if len > 0:
        v = r.rpop(KEY)
        myvar = myobj.add_variable(idx, "MyVariable", str(v))
    else:
        myvar = myobj.add_variable(idx, "MyVariable", '')

    #myvar.set_writable()    # Set MyVariable to be writable by clients
    server.iserver.history_manager.set_storage(HistorySQLite('history.db'))
    server.start()
    server.historize_node_data_change(myvar, period=None, count=1000)

    #------------------------
    # data injecting loop
    #------------------------
    while True:
        try:
            len = r.llen(KEY)
            print('len:',len)
            if (len > 0):
                v = r.rpop(KEY)
                print('v:',v)
                myvar.set_value(v)    
            else:
                print('no data,waiting...')
                time.sleep(0.1)

        except Exception as e:
            try:
                r.close()
                r = redis.Redis(host=HOST, port=6379, db=0)
            except:
                pass
            print('exception:',str(e))        
            break
            



