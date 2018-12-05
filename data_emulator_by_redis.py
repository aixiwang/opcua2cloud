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
        try:
            r.lpush(KEY,'test data')
            time.sleep(10)
            
        except Exception as e:
            print('exception:',str(e))
            pass