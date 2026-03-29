import json
import os
import threading
import time
import pika

from app.services.order_store import update_order_status

# IMPORTANTE: dentro do Docker use "rabbitmq"
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_PAYMENT_PROCESSED = "payment_processed"


def consume_payment_processed():
    while True:
        try:
            print(f"[ORDER] Trying to connect to RabbitMQ at {RABBITMQ_HOST}...")

            params = pika.ConnectionParameters(host=RABBITMQ_HOST)
            connection = pika.BlockingConnection(params)
            channel = connection.channel()

            channel.queue_declare(queue=QUEUE_PAYMENT_PROCESSED, durable=True)

            print(f"[ORDER] Connected. Waiting for '{QUEUE_PAYMENT_PROCESSED}' messages...")

            def callback(ch, method, properties, body):
                event = json.loads(body)
                print(f"[ORDER] Received event: {event}")

                if event.get("event_type") != "PaymentProcessed":
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    return

                order_id = event["order_id"]
                payment_status = event["payment_status"]

                if payment_status == "APPROVED":
                    update_order_status(order_id, "CONFIRMED")
                    print(f"[ORDER] Order {order_id} → CONFIRMED")
                else:
                    update_order_status(order_id, "PAYMENT_FAILED")
                    print(f"[ORDER] Order {order_id} → PAYMENT_FAILED")

                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue=QUEUE_PAYMENT_PROCESSED,
                on_message_callback=callback,
            )

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("[ORDER] RabbitMQ not ready. Retrying in 5 seconds...")
            time.sleep(5)

        except Exception as e:
            print(f"[ORDER] Unexpected error: {e}")
            time.sleep(5)


def start_payment_result_consumer():
    thread = threading.Thread(target=consume_payment_processed, daemon=True)
    thread.start()