import pika
import json
import os
import time
from executor import execute_function

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def callback(ch, method, properties, body):
    message = json.loads(body)
    execute_function(message)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def connect_to_rabbitmq():
    while True:
        try:
            print("Connecting to RabbitMQ...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            print("Connected to RabbitMQ")
            return connection
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            
try:
    print("Starting Container Manager Worker...")
    connection = connect_to_rabbitmq()
except KeyboardInterrupt:
    print("Shutting down gracefully...")
    exit(0)


channel = connection.channel()
channel.queue_declare(queue="function_invocations", durable=True)

channel.basic_consume(
    queue="function_invocations",
    on_message_callback=callback
)

print("Container Manager listening for invocations...")
channel.start_consuming()
