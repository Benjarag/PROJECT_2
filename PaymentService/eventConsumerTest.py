import pika

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    print("Success")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='order_events', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    
    queue_name = result.method.queue

    channel.queue_bind(exchange='order_events', queue=queue_name)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == "__main__":
    main()