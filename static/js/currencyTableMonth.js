const labels = historicalData.map(data => new Date(data.time * 1000).toLocaleDateString());
const data = historicalData.map(data => data.close);

const ctx = document.getElementById('rateCharMonth').getContext('2d');
const cryptoChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: `${fromCurrency} to ${toCurrency}`,
            data: data,
            borderColor: 'rgb(45,143,160)',
            pointRadius: 0
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: false,
                ticks: {
                    color: 'white'
                }
            },
            x: {
                ticks: {
                    color: 'white'
                }
            },
        },
        plugins: {
            legend: {
                labels: {
                    color: 'white'
                }
            },
            tooltip: {
                enabled: true,
                mode: 'index',
                intersect: false,
                position: 'nearest',
            }
        },

    }
});