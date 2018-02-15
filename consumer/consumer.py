import pika
import psycopg2
import time

timeout = 0.01
try:
    pika_conn = pika.BlockingConnection( 
      pika.URLParameters("amqp://guest:guest@queue:5672") 
    )
    postgres_conn = psycopg2.connect("dbname=queue user=consumer host=database")
except:
    success = False
    while not success:
        try:
            time.sleep(timeout)
            timeout *= 2
            pika_conn = pika.BlockingConnection( 
              pika.URLParameters("amqp://guest:guest@queue:5672") 
            )
            postgres_conn = psycopg2.connect("dbname=queue user=consumer host=database")
            success = True
        except:
            success = False


channel = pika_conn.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    recieved = (body.decode())
    cursor = postgres_conn.cursor()
    cursor.execute("INSERT INTO queue VALUES (DEFAULT, %s)", (recieved,))
    postgres_conn.commit()
    cursor.close()

channel.basic_consume(callback,
            queue='hello',
            no_ack=True)
channel.start_consuming()

postgress_conn.close()
pika_conn.close()
