# Real-Time-Financial-Data-Analysis

## Overview

The Real-Time-Financial-Data-Analysis project is designed to create a scalable and distributed system for processing and analyzing simulated financial data. The system consists of various components, including data generation, data ingestion, stream processing, signal generation, notification, data aggregation and visualization. The ultimate goal is to provide users with actionable trading signals and real-time financial insights.

## Components

### 1. Data Generation
Simulated financial data is generated using the Data Generator Script. This script produces realistic financial market scenarios to test the functionality of the system.

### 2. Data Ingestion
The Data Ingestion component validates and sends the simulated financial data to the Stream Processing Service. This ensures that only accurate and valid data is processed further in the system.

### 3. Stream Processing
The Stream Processing component is responsible for processing the incoming financial data in real-time. It calculates mandatory trading indicators, facilitating the generation of meaningful insights.

### 4. Signal Generation
Buy/sell signals are generated based on the processed data, and these signals are sent to the Notification Service. This step enables users to receive instant notifications about trading opportunities.

### 5. Notification
The Notification Service delivers real-time trading signals to users, ensuring that they stay informed and can make timely decisions. Notifications can be configured to reach users through various channels, such as email or mobile applications.

### 6. Data Aggregation
Data Aggregation involves summarizing and aggregating the processed financial data. This step provides an overview and insights into the overall market trends and conditions.

### 7. Visualization
The Visualization component displays real-time financial data and generated signals on a user-friendly dashboard. This enables users to quickly grasp the current market situation and make informed decisions.


## Mandatory Trading Indicators

We have used the following trading indicators must for this project:

1. **Moving Average (MA):** Helps identify the direction of the trend by averaging the closing prices of stocks over a specified number of periods.

2. **Exponential Moving Average (EMA):** Reacts more quickly to price changes than the simple moving average by giving more weight to the most recent prices.

3. **Relative Strength Index (RSI):** Measures the speed and change of price movements to identify overbought or oversold conditions in the market.




## Tools Used

- **Apache Kafka:** Used for building a distributed streaming platform to handle real-time financial data.
  
- **Back-end:** 
  - **Python:** Primary programming language for backend development.
  - **Fast API:** Fast API is used to create a high-performance backend API for real-time data processing.

- **Cache:**
  - **Redis:** Utilized as an in-memory data store for caching frequently accessed data, improving system performance.

- **Database:**
  - **SQLite:** Chosen as the database system for its lightweight nature, suitable for the project's needs.

- **Front-end:**
  - **HTML, CSS, and JavaScript:** Used to develop a responsive and interactive user interface for the real-time dashboard.

- **Containerization:**
  - **Docker:** Implemented for containerizing the application components, ensuring consistency across different environments.

- **Orchestration:**
  - **Kubernetes:** Employed for container orchestration, enabling efficient management and scaling of the application.
  - **Minikube:** Used for local Kubernetes cluster setup during development and testing.
