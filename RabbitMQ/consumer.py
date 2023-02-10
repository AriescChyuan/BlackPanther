import pika
import threading
import time
import json

TARGET_LOCATION = {
    "latitude": 0,
    "longitude" : 0,
    "altitude" : 0
}

credentials = pika.PlainCredentials("Bruce", "19920321")
parameters = pika.ConnectionParameters("localhost",
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
# channel.queue_declare(queue='Test')
data = ""
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
t = threading.Thread(target = recv_data)

# 執行該子執行緒
t.start()

#主執行緒
while True:
    try:
        if data != None:
            if type(data) == bytes:
                data = data.decode('utf8')
                data = json.loads(data)

                TARGET_LOCATION["latitude"] = data["latitude"]
                TARGET_LOCATION["longitude"] = data["longitude"]
                TARGET_LOCATION["altitude"] = data["altitude"]

                print(TARGET_LOCATION)
                time.sleep(1)
    except KeyboardInterrupt:
        channel.close()
        break