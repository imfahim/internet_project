
const labels = historicalData.map(data => new Date(data.time * 1000).toLocaleDateString());
const data = historicalData.map(data => data.close);

const ctx = document.getElementById('rateCharMonth').getContext('2d');
const cryptoChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: `${toCurrency} to ${fromCurrency}`,
            data: data,
            borderColor: 'rgb(75, 192, 192)',
            pointRadius: 0
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});