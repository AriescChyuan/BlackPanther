# import pymavlink.mavutil as utility
import time
import threading
import pika
import json
from mavlink_func import Mavlink

AUTO_OPTIONS_PARAM = "AUTO_OPTIONS"

TARGET_LOCATION = {
    "latitude": 0,
    "longitude" : 0,
    "altitude" : 0
}

current_location ={
    "latitude": 0.0,
    "longitude" : 0.0
}

target_location= {
    "latitude": 0.0,
    "longitude" : 0.0,
    "distance" : 0.0
}

# ---------雷達相關-------- 
# remote_host = '192.168.1.2'
# exchange_name = 'api-event'
# binding_key = "t_meta.surveillance.task.*.targets.updated"

# connection = pika.BlockingConnection( 
#     pika.ConnectionParameters(host=remote_host)) 
# channel = connection.channel()
# result = channel.queue_declare('', exclusive=True) 
# queue_name = result.method.queue 
# channel.queue_bind(
# exchange=exchange_name, queue=queue_name, routing_key=binding_key)
# -------------------------
credentials = pika.PlainCredentials("Bruce", "19920321")
parameters = pika.ConnectionParameters("localhost",
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
# channel.queue_declare(queue='Test')
data = ""
def catch_target_coordinate_sim(data):
    if data != None:
            if type(data) == bytes:
                data = data.decode('utf8')
                data = json.loads(data)

                TARGET_LOCATION["latitude"] = data["latitude"]
                TARGET_LOCATION["longitude"] = data["longitude"]
                TARGET_LOCATION["altitude"] = data["altitude"]

def catch_target_coordinate_radar(data):
    data = json.loads(data)
    if data != None:
        target_type_date = data['data']['targets_updated'][0]['target_type']
        state_time_pair_data = data['data']['targets_updated'][0]['state_time_pairs']

        if target_type_date == -1:
            print('目標物消失:')
        elif target_type_date == 0:
            print('偵測無法辨識物體')
        elif target_type_date == 1:
            print('偵測到無人機')
        elif target_type_date == 2:
            print('偵測到鳥類')
        elif target_type_date == 3:
            print('偵測到飛機')

        if state_time_pair_data != None:

            TARGET_LOCATION["latitude"] = state_time_pair_data[0]['position']['lat']
            TARGET_LOCATION["longitude"] = state_time_pair_data[0]['position']['lng']
            TARGET_LOCATION["altitude"] = state_time_pair_data[0]['position']['alt']
            print('經度：{}'.format(TARGET_LOCATION["latitude"]))
            print('緯度：{}'.format(TARGET_LOCATION["longitude"]))
            print('高度：{}'.format(TARGET_LOCATION["altitude"]))
# 多執行緒
def recv_data():
    def callback(ch, method, properties, body):
        # print('[x] Received %r' % body)
        global data
        data = body

    channel.basic_consume(
        queue='Test',  
        on_message_callback=callback,  
        auto_ack=True)  
    print('[*] Waiting for message.')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
# 建立一個子執行緒
catch_radar_data = threading.Thread(target = recv_data)
# 執行該子執行緒
catch_radar_data.start()


if __name__ == "__main__":
    vehicle = Mavlink("udpin:127.0.0.1:14550")
    vehicle.set_param(AUTO_OPTIONS_PARAM, 7)
    # get_param(AUTO_OPTIONS_PARAM)

    while True:
        res = vehicle.set_mode("GUIDED")
        if res == "accepted":
            break
        time.sleep(1)

    while True: 
        sensor_status = vehicle.hearth_check()  
        if sensor_status:
            print("Vehicle is armable!")
            break
        else:
            print("Vehicle is unarmable!")
        time.sleep(1)
        
    vehicle.arm_disarm(1)
    vehicle.takeoff(10)
    while True:
        try:
            catch_target_coordinate_sim(data)
            # catch_target_coordinate_radar(data)
            vehicle.goto(TARGET_LOCATION)

        except KeyboardInterrupt:
            res = vehicle.set_mode("RTL")
            if res == "accepted":
                break

    
    
        
        


