import threading
import time
import requests
import socket
import random
import json

# Thread function for testing localhost:5000/data/?stock (redis caching) to initialize charts with data from an hour ago till now
def get_stock_data():
    while True:
        stock_list = ["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA"]
        stock = random.choice(stock_list)
        try:
            response = requests.get(f"http://localhost:8500/data/?stock={stock}")
            print(response.json())
            print("\n\n ****************************************   \n\n")
        except requests.RequestException as e:
            print(f"Error fetching stock data: {e}")
        time.sleep(90)

# Thread function for testing localhost:7000/summary/ to get stock summary(number of buy and sell signals for that stock)
def get_summary_data():
    while True:
        try:
            response = requests.get("http://localhost:7000/summary/")
            print(response.text)
            print("\n\n ****************************************   \n\n")
        except requests.RequestException as e:
            print(f"Error fetching summary data: {e}")
        time.sleep(30)

# Thread function for receiving data via socket to retrive real-time data including (signal or closing-prices)
def socket_receive_json():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("localhost", 12345))
            while True:
                data = s.recv(4096)
                if not data:
                    break
                data_dict = json.loads(data.decode('utf-8'))
                print(data_dict)
                # print({'datetime': data_dict['timestamp'], 'closing price': data_dict['closing_price']})
                print("\n\n ****************************************   \n\n")

        except socket.error as e:
            print(f"Socket error: {e}")


# Creating threads
thread1 = threading.Thread(target=get_stock_data)
thread2 = threading.Thread(target=get_summary_data)
thread3 = threading.Thread(target=socket_receive_json)

# Starting threads
thread1.start()
thread2.start()
thread3.start()

# Joining threads to the main thread
thread1.join()
thread2.join()
thread3.join()
