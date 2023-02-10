import pika
import time
import circle_path
credentials = pika.PlainCredentials("Bruce", "19920321")
parameters = pika.ConnectionParameters("localhost",
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
# channel.queue_declare(queue='hello') # 宣告一個名為 'hello' 的訊息佇列

radius = 0.1
center_lat = -35.36323458
center_lon = 149.16522392
coordinates = []


print(f" [x] Sent~")
while True:

    # 建立圓形座標路經 10個點位

    for i in range(10):
        angle = i * 36
        lat, lon = circle_path.get_coordinate(radius, center_lat, center_lon, angle)
        coordinates.append((lat, lon))

    for i in range(10):
        print(coordinates[i][0], coordinates[i][1])
        data = "{\"latitude\": " + str(coordinates[i][0]) + ",\"longitude\" : " + str(coordinates[i][1]) + ",\"altitude\" : 30}"
    
        data = str(data)
        print(data)
        # 把訊息放進名稱為：hello 的佇列中
        channel.basic_publish(exchange='',routing_key='Test',body=data)
        time.sleep(5)

connection.close()