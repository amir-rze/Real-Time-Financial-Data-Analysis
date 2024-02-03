import socket
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import asyncio
from config import KAFKA_BOOTSTRAP_SERVERS,SIGNAL_KAFKA_TOPIC

clients = set()

logging.basicConfig(level=logging.INFO)

async def client_handler(reader, writer):
    clients.add(writer)
    try:
        while True:
            # Here, you could add logic to receive data from the client if needed
            await asyncio.sleep(1)  # Prevent the loop from closing immediately
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def broadcast_signal(msg):
    for writer in list(clients):
        try:
            writer.write(msg.encode('utf-8'))
            await writer.drain()
            logging.info("Signal sent to client!")
        except :
            clients.remove(writer)
            writer.close()
            logging.info("Client connection closed.")


async def read_data():
    consumer = AIOKafkaConsumer(
        SIGNAL_KAFKA_TOPIC,
        loop=asyncio.get_event_loop(),
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for message in consumer:
            data = message.value
            logging.info("Notification Service received data!")
            msg = f"{data['signal']} {data['stock_symbol']} shares !!!"
            await broadcast_signal(msg)
    finally:
        await consumer.stop()

async def start_server(host, port):
    server = await asyncio.start_server(client_handler, host, port)
    logging.info(f'Server is listening on {port}...')
    async with server:
        await server.serve_forever()

async def main():
    await asyncio.gather(
        start_server('localhost', 12345),
        read_data(),
    )

if __name__ == '__main__':
    asyncio.run(main())