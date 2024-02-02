import asyncio


# env variables

# Define the Kafka bootstrap servers
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
DATA_KAFKA_TOPIC = "stock-data"
ADDITIONAL_DATA_KAFTA_TOPIC = "stock-additional-data"

LOOP = asyncio.get_event_loop()


# Define the Redis URL
REDIS_URL = "redis://localhost:6379"
