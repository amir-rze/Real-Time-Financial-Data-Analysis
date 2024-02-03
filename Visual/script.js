document.addEventListener('DOMContentLoaded', function() {
    loadRealTimeDataPage()
});


function loadRealTimeDataPage() {
    const content = document.getElementById('content');
    content.innerHTML = '<h2>Real-Time Data</h2><div id="charts"></div>';
    const chartsDiv = document.getElementById('charts');

    stocks.forEach(stock => {
        const chartContainer = document.createElement('div');
        chartContainer.id = stock;
        chartContainer.innerHTML = `<h3>${stock}</h3><canvas id="${stock}-chart"></canvas>`;
        chartsDiv.appendChild(chartContainer);

        fetchInitialData(stock);
    });

    setupNotificationSocket();
}

function fetchInitialData(stock) {
    fetch(`http://localhost:5000/data/?stock=${stock}`)
        .then(response => response.json())
        .then(data => {
            setupChart(stock, data);
            setupWebSocket(stock);
        })
        .catch(error => console.error('Error fetching initial data:', error));
}

function setupChart(stock, initialData) {
    const ctx = document.getElementById(`${stock}-chart`).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: initialData.map(item => item.datetime),
            datasets: [{
                label: `${stock} Closing Price`,
                data: initialData.map(item => item.closing_price),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute'
                    }
                },
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function setupWebSocket(stock) {
    const socket = new WebSocket('ws://localhost:5000/ws');

    socket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.stock === stock) {
            // Code to update the chart with new data
        }
    };
}

function setupNotificationSocket() {
    const notificationSocket = new WebSocket('ws://localhost:12345');
    notificationSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        // Display notification
        alert(`Notification: ${data.message}`);
    };
}