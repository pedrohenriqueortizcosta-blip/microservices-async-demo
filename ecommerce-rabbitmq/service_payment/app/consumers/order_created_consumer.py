import json
import os
import random
import threading
import time
import pika

from app.services.broker import publish_payment_processed
from app.services.payment_store import create_payment

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_ORDER_CREATED = "order_created"


def consume_order_created():
    while True:
        try:
            print(f"Trying to connect to RabbitMQ at host={RABBITMQ_HOST}...")
            params = pika.ConnectionParameters(host=RABBITMQ_HOST)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE_ORDER_CREATED, durable=True)
            print(f"Connected to RabbitMQ. Waiting for messages in '{QUEUE_ORDER_CREATED}'")

            def callback(ch, method, properties, body):
                event = json.loads(body)
                print(f"Received event: {event}")

                if event.get("event_type") != "OrderCreated":
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                order_id = event["order_id"]
                customer_id = event["customer_id"]
                amount = event["amount"]

                time.sleep(3)

                approved = random.choice([True, True, True, False])
                payment_status = "APPROVED" if approved else "DECLINED"

                payment = create_payment(order_id, customer_id, amount, payment_status)
                print(f"Payment created: {payment}")

                publish_payment_processed(
                    {
                        "event_type": "PaymentProcessed",
                        "order_id": order_id,
                        "payment_status": payment_status,
                    }
                )
                print(f"Published PaymentProcessed for order {order_id}")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue=QUEUE_ORDER_CREATED,
                on_message_callback=callback,
            )

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("RabbitMQ not ready yet. Retrying in 5 seconds...")
            time.sleep(5)

        except Exception as e:
            print(f"Unexpected error in payment consumer: {e}")
            time.sleep(5)


def start_order_created_consumer():
    thread = threading.Thread(target=consume_order_created, daemon=True)
    thread.start()