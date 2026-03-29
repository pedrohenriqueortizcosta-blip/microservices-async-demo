🛒 E-commerce Microservices (Order & Payment)
📌 Overview

This project is a simple e-commerce backend built using a microservices architecture with asynchronous communication.

It demonstrates how two independent services — order and payment — communicate through a message broker to process orders in a decoupled and scalable way.

🧠 Architecture
Client → service_order → RabbitMQ → service_payment → RabbitMQ → service_order
Flow:
A client creates an order via service_order
The order is saved with status PENDING_PAYMENT
An event OrderCreated is published to RabbitMQ
service_payment consumes the event
Payment is processed (simulated)
A PaymentProcessed event is published
service_order consumes the result and updates the order status
⚙️ Technologies Used
FastAPI → API development
Uvicorn → server for FastAPI
RabbitMQ → async communication
Docker → containerization
Docker Compose → multi-service setup
Pika → messaging client
📦 Services
🧾 service_order
Handles order creation and retrieval
Publishes OrderCreated events
Consumes PaymentProcessed events
Updates order status
💳 service_payment
Consumes OrderCreated events
Simulates payment processing
Publishes PaymentProcessed events
Stores processed payments
🚀 Getting Started
1. Clone the repository
git clone <https://github.com/pedrohenriqueortizcosta-blip/microservices-async-demo.git>
cd ecommerce-rabbitmq
2. Start the services
docker compose up --build
3. Access services
Service	URL
Order API	http://localhost:8001/docs

Payment API	http://localhost:8002/docs

RabbitMQ UI	http://localhost:15672

RabbitMQ credentials:

user: guest
pass: guest
🧪 Testing the Flow
1. Create an order

Use Swagger (/docs) or:

curl -X POST http://localhost:8001/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "product_id": 101,
    "quantity": 2,
    "amount": 199.90
  }'
2. Check order status
GET /orders/{order_id}

Initial state:

PENDING_PAYMENT

After processing:

CONFIRMED

or

PAYMENT_FAILED
3. Check payments
GET http://localhost:8002/payments
📊 RabbitMQ Monitoring

Access:

http://localhost:15672

Key concepts:

Ready → messages waiting to be consumed
Unacked → messages being processed
Consumers → active consumers
🧠 Key Concepts Demonstrated
Microservices architecture
Asynchronous communication
Event-driven design
Message queues
Decoupled services
Retry logic for resilience
⚠️ Notes
Data is stored in memory (no database)
Payment processing is simulated
Not production-ready (educational purpose)
🔥 Future Improvements
Add PostgreSQL for persistence
Implement retry & dead-letter queues
Add authentication (JWT)
Add API Gateway
Deploy on AWS (ECS / EKS)
🧠 Learning Goal

This project is designed to help understand:

how APIs communicate asynchronously
how message brokers work
how microservices interact in real systems
📌 Summary

This project simulates a real-world e-commerce flow using asynchronous microservices with RabbitMQ, demonstrating how systems can scale and remain loosely coupled.