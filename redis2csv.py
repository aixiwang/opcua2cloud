import sys
#sys.path.insert(0, "..")
import time
import redis

HOST = '180.76.242.57'
KEY = 'xxx' 
#-------------------
# writefile2
#-------------------
def writefile2(filename,content):
    f = open(filename,'ab')
    if type(content) == str:
        content_bytes = content.encode('utf-8')
        f.write(content_bytes)
    else:
        f.write(content)
    f.flush()
    f.close()
    return
    
if __name__ == "__main__":
    r = redis.Redis(host=HOST, port=6379, db=0)
    #print('connected to redis')
    while True:
        len = r.llen(KEY)
        #print('len:',len)
        if (len > 0):
            v = r.rpop(KEY)
            #print('v:',v)
            writefile2(KEY + '.csv',v + '\r\n')
        else:
            print('complted')
            break
