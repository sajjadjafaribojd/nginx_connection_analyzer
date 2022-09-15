from datetime import datetime,timedelta
import json
import threading,requests


def send_request():
    url={'http://10.10.10.10/nginx_status':'nginx_connection_ny.json'}
    for key,value in url.items():
        headers = {'user-agent': 'JabJ'}
        try:
            res=requests.get(key,headers=headers,)
            result={}
            if res:
                active_connection=res.text.partition('\n')[0]  #keep firest line and remmove other line.#https://docs.python.org/3/library/stdtypes.html#str.partition
                active_connection=active_connection.split(' ') #split string by space. ['Active', 'connections:', '32', '']
                active_connection_count=active_connection[2]   #Select index 2 from befor array. 32
                result[str(datetime.utcnow())]=str(active_connection_count)
                write_to_file(json.dumps(result),value)
                return json.dumps(result)   
            else:
                return('error',res.status_code)

        except Exception as e:
                return e 
         


def write_to_file(output,address):
    try:
        f=open(address,"a")
        f.write(output+",")
        f.close()
        return True
    except Exception as e:
            return e
        
def printit_0(): #This function run every 5 second.
  threading.Timer(5.0, printit_0).start()
  print(send_request())
#printit_0()

def convert_utc_to_tehran(dic_time):
    try:
        convert_str_to_datetime_format=datetime.strptime(dic_time,'%H:%M:%S')
        new_time = convert_str_to_datetime_format+ timedelta(minutes=30, hours=4)
        return new_time.time()
    except Exception as e:
            return e

def find_max_min_connection(address,min_max):
    dic={}
    f=open(address,'r')
    var=json.load(f)
    for value in var:
        for key,value in value.items():
            var=key.split(' ') 
            var=var[1].split('.')
            new_key=convert_utc_to_tehran(var[0])
            dic[str(new_key)]=int(value) #if str can not find max value. first we should convert to srt

    if min_max == 'max':
        max_key = max(dic, key=dic.get)
        f.close()
        return [max_key,dic[max_key]]
    elif min_max == 'min':
        min_key = min(dic, key=dic.get)
        f.close()
        return [min_key,dic[min_key]]
    else:
        return False               
   
         
# print('Max_USA_Newyork:',find_max_min_connection('nginx_connection_ny.json','max'))
# print('Min_USA_Newyork:',find_max_min_connection('nginx_connection_ny.json','min'))

