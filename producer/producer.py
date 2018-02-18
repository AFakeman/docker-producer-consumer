import pika

connection = pika.BlockingConnection(  
    pika.URLParameters("amqp://guest:guest@queue:5672") 
)
channel = connection.channel() 
channel.queue_declare(queue='hello') 
data = input()
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=data.encode()  
)
connection.close()
