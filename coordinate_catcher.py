#!/usr/bin/env python
# pika is required. you should've installed pika first. 
import pika
import sys
import json
remote_host = '192.168.1.2'
exchange_name = 'api-event'
binding_key = "t_meta.surveillance.task.*.targets.updated"

AUTO_OPTIONS_PARAM = "AUTO_OPTIONS"

# location for testing
TARGET_LOCATION = {
    "latitude": -35.36130812,
    "longitude" : 149.16114736,
    "altitude" : 30
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

connection = pika.BlockingConnection( 
    pika.ConnectionParameters(host=remote_host)) # connect to edge
channel = connection.channel() # create a channel
# Applications may pick queue names or ask the broker to generate a name for them. # Queue names may be up to 255 bytes of UTF-8 characters.
# An AMQP 0-9-1 broker can generate a unique queue name on behalf of an app.
# To use this feature, pass an empty string as the queue name argument.
# The generated name will be returned to the client with queue declaration response.
result = channel.queue_declare('', exclusive=True) # declare a queue with empty name to ask the broker to generate a name 
queue_name = result.method.queue # get queue_name
channel.queue_bind(
exchange=exchange_name, queue=queue_name, routing_key=binding_key) # bind queue
# declare a callback to process(consume) data from RabbitMQ 
def callback(ch, method, properties, body):
    data = json.loads(body)
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
            latitude_data = state_time_pair_data[0]['position']['lat']
            longitude_data = state_time_pair_data[0]['position']['lng']
            altitude_data = state_time_pair_data[0]['position']['alt']
            print('經度：{}'.format(latitude_data))
            print('緯度：{}'.format(longitude_data))
            print('高度：{}'.format(altitude_data))
        print('__________________________')
channel.basic_consume(
queue=queue_name, on_message_callback=callback, auto_ack=True)
print('接收訊息中...')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

