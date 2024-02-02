import socket
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import asyncio
from config import KAFKA_BOOTSTRAP_SERVERS,SIGNAL_KAFKA_TOPIC

clients = []

logging.basicConfig(level=logging.INFO)

# port = 12345

# async def read_and_send_data():

#     loop = asyncio.get_event_loop()
#     consumer = AIOKafkaConsumer(
#         SIGNAL_KAFKA_TOPIC,loop=loop,
#         bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#         value_deserializer=lambda m: json.loads(m.decode('utf-8'))
#     )
#     await consumer.start()
#     try:
#         async for message in consumer:
#             data = message.value
#             logging.info("Notification Service received data ! ")
#             for client in clients:
#                 msg = f"{data['signal']} {data['stock_symbol']} shares !!! "
#                 client.sendall(msg.encode('utf-8'))
#                 logging.info(f"signal sent to client {client} ! ")

#     finally:
#         consumer.stop()


# def accept_connections(ServerSocket):
#     while True:
#         Client, address = ServerSocket.accept()
#         logging.info('Connected to: ' + address[0] + ':' + str(address[1]))
#         clients.append(Client)


# async def start_server(host, port):
#     ServerSocket = socket.socket()
#     try:
#         ServerSocket.bind((host, port))
#     except socket.error as e:
#         logging.error(str(e))

    
#     logging.info(f'Server is listing on the port {port}...')
#     ServerSocket.listen(5)
#     await accept_connections(ServerSocket)


# async def main():
#     # Start the server and the read/send coroutine concurrently
#     await asyncio.gather(
#         start_server('localhost', 12345),
#         read_and_send_data(),
#     )

# if __name__ == '__main__':
#     asyncio.run(main())



async def client_handler(reader, writer):
    clients.append(writer)
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

async def broadcast_messages():
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
            for writer in clients:
                writer.write(msg.encode('utf-8'))
                await writer.drain()  # Ensure the message is sent
                logging.info("Signal sent to client!")
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
        broadcast_messages(),
    )

if __name__ == '__main__':
    asyncio.run(main())