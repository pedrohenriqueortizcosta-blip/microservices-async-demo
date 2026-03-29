import json
import os
import pika

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_ORDER_CREATED = "order_created"
QUEUE_PAYMENT_PROCESSED = "payment_processed"


def get_connection():
    params = pika.ConnectionParameters(host=RABBITMQ_HOST)
    return pika.BlockingConnection(params)


def publish_order_created(event: dict) -> None:
    connection = get_connection()
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_ORDER_CREATED, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_ORDER_CREATED,
        body=json.dumps(event),
    )

    connection.close()