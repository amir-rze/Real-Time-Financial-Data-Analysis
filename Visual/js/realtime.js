document.addEventListener('DOMContentLoaded', function() {
    // Safely initialize WebSocket connections within try-catch blocks
    try {
        const ws = new WebSocket('ws://localhost:5000/ws');
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            // Assuming data contains { stock: 'STOCK_SYMBOL', datetime: 'DATETIME', closing_price: PRICE }
            if (chart && data.stock === chart.data.datasets[0].label.split(' ')[0]) {
                updateChart(data);
            }
        };
    } catch (error) {
        console.error('WebSocket connection failed:', error);
    }

    try {
        const notificationsWs = new WebSocket('ws://localhost:12345');
        notificationsWs.onmessage = function(event) {
            const notification = JSON.parse(event.data);
            alert('Notification: ' + notification.message);
        };
    } catch (error) {
        console.error('WebSocket connection failed:', error);
    }
});

let chart; // Global variable to hold the chart instance

function initChart(stockSymbol, labels, closingPrices) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    if (chart) {
        chart.destroy();
    }
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `${stockSymbol} Closing Price`,
                data: closingPrices,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        tooltipFormat: 'll HH:mm'
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Closing Price'
                    }
                }
            }
        }
    });
}

function fetchStockData(stockSymbol) {
    fetch(`http://localhost:5000/data/?stock=${stockSymbol}`)
        .then(response => response.json())
        .then(data => {
            // Assuming data is an array of { datetime, closing_price }
            const labels = data.map(item => item.datetime);
            const closingPrices = data.map(item => item.closing_price);
            initChart(stockSymbol, labels, closingPrices);
        })
        .catch(error => console.error('Error fetching stock data:', error));
}

function updateChart(data) {
    // Add new data point to the chart
    chart.data.labels.push(data.datetime);
    chart.data.datasets[0].data.push(data.closing_price);
    chart.update();
}
