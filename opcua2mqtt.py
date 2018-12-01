import sys
#sys.path.insert(0, "..")
import time

from opcua import Client
#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.publish as publish
import awsiot
import redis

MQTT_MODE = 'simple' # simple,simplewithpass,awsiot
AWSIOT_AK = 'test'
AWSIOT_SK = 'test'
HOST = '180.76.242.57'
SAVE_TO_REDIS_EN = True
#------------------------
# normal_mqtt_publish
#------------------------
def normal_mqtt_publish(topic,payload):
    try:
        publish.single(topic, payload, hostname='m2m.eclipse.org')
        print('publish data to m2m.eclipse.org opcua2mqtt/ topic')
    except Exception as e:
        print('normal_mqtt_publish exception:',str(e))
        
#------------------------
# awsiot_mqtt_publish
#------------------------
def awsiot_mqtt_publish(topic,payload):
    try:
        client = awsiot.awsiot_client(access_key = AWSIOT_AK, secret_key = AWSIOT_SK)
        client.publish(topic, payload)

    except Exception as e:
        print('awsiot_mqtt_publish exception:',str(e))
        
        
if __name__ == "__main__":


    client = Client("opc.tcp://" + HOST + ":4840/freeopcua/server/")
    #client = Client("opc.tcp://localhost:4840/freeopcua/server/")    
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    r = redis.Redis(host=HOST, port=6379, db=0)
    
    while True:
        try:
            client.connect()

            # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
            root = client.get_root_node()
            print("Objects node is: ", root)

            # Node objects have methods to read and write node attributes as well as browse or populate address space
            print("Children of root are: ", root.get_children())

            # get a specific node knowing its node id
            #var = client.get_node(ua.NodeId(1002, 2))
            #var = client.get_node("ns=3;i=2002")
            #print(var)
            #var.get_data_value() # get value of node as a DataValue object
            #var.get_value() # get value of node as a python builtin
            #var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
            #var.set_value(3.9) # set node value using implicit data type

            # Now getting a variable node using its browse path
            myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
            obj = root.get_child(["0:Objects", "2:MyObject"])
            
            client.disconnect()            
            print("myvar is: ", myvar)
            print("myobj is: ", obj)

            
            #-------------------------
            # save opc ua data redis
            #-------------------------
            if SAVE_TO_REDIS_EN == True:
                try:
                    l = r.lpush('opcua_001',str(myvar))
                    print('save opcua data to redis, ret=',l)
                except Exception as e:
                    print('save opcua data to redis exception:',str(e))            
                    try:
                        r.close()
                        r = redis.Redis(host=HOST, port=6379, db=0)
                    except:
                        pass

            # Stacked myvar access
            # print("myvar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())

            if MQTT_MODE == 'simple':
                normal_mqtt_publish('opcua2mqtt/',str(myvar))
                
            elif MQTT_MODE == 'awsiot':
                awsiot_mqtt_publish('opcua2mqtt/',str(myvar))
            
            else:
                print('no valid mqtt_mode defined')
                
        except Exception as e:
            print('exception 2:',str(e))
            try:
                client.disconnect()
            except:
                pass
        
        time.sleep(5)
        
