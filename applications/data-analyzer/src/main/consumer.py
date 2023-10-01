import pika
from app import analyze_all_listings

def callback(ch, method, properties, body):
    body = json.loads(body)
    print(" [x] Received %r" % body)
    analyze_all_listings()

def consume():
    # Message Queue
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=36000))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    channel.queue_declare(queue='analyze')
    channel.basic_consume(queue='analyze', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    # End of Message Queue code
