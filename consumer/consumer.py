import pika
import psycopg2

while True:
    try:
        pika_conn = pika.BlockingConnection( 
          pika.URLParameters("amqp://guest:guest@queue:5672") 
        )
    finally:
        break

postgres_conn = psycopg2.connect("dbname=queue user=consumer host=database")

channel = pika_conn.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    recieved = (body.decode())
    cursor = postgres_conn.cursor()
    print(recieved)
    cursor.execute("INSERT INTO queue VALUES (DEFAULT, %s)", (recieved,))
    postgres_conn.commit()
    cursor.close()

channel.basic_consume(callback,
            queue='hello',
            no_ack=True)
channel.start_consuming()
