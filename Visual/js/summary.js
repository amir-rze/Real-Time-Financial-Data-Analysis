document.addEventListener('DOMContentLoaded', function() {
    fetchSummaryData();
});

function fetchSummaryData() {
    fetch('http://localhost:7000/summary/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            console.log(response)
            return response.json();
        })
        .then(data => {
            displaySummaryData(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
            // Optionally, insert a row or a message in the table indicating the error
            const tableBody = document.getElementById('summaryTable').getElementsByTagName('tbody')[0];
            tableBody.innerHTML = `<tr><td colspan="3">Error fetching data</td></tr>`;
        });
}

function displaySummaryData(data) {
    const tableBody = document.getElementById('summaryTable').getElementsByTagName('tbody')[0];
    // Clear existing table data
    tableBody.innerHTML = '';

    // Iterate over each item in the data array and add a row to the table
    data.forEach(stock => {
        const row = tableBody.insertRow();
        const stockCell = row.insertCell(0);
        const sellCountCell = row.insertCell(1);
        const buyCountCell = row.insertCell(2);

        stockCell.textContent = stock.stock_symbol;
        sellCountCell.textContent = stock.sell_count;
        buyCountCell.textContent = stock.buy_count;
    });
}
