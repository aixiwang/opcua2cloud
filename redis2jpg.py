import sys
#sys.path.insert(0, "..")
import time
import redis
import binascii

HOST = '180.76.242.57'
KEY = 'CAM-8D7D3ADC8534'
KEY2 = KEY + '-file'
JPG_ROOT_DIR = '/root/jpg/'
 
#-------------------
# writefile
#-------------------
def writefile(filename,content):
    f = open(filename,'wb')
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
            len = r.llen(KEY)
            #print('len:',len)
            if (len > 0):
                v = r.rpop(KEY)
                #print('v:',type(v),v)
                 
                v_bin = binascii.unhexlify(v)
                time_str = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
                f_name = JPG_ROOT_DIR + KEY + '-' + time_str + '.jpg'

                r.lpush(KEY2,f_name)
                writefile(f_name,v_bin)
                print('save value to:',f_name)

            else:
                #print('=')
                time.sleep(1)
                
        except Exception as e:
            print('exception:',str(e))

            try:
                r.close()
            except:
                pass
             
            try:
                r = redis.Redis(host=HOST, port=6379, db=0)
            except:
                pass
            
            time.sleep(0.1)                
            break
