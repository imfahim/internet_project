let rateChart;
let chartData = {
    labels: [],
    datasets: [{
        label: `${fromCurrency} to ${toCurrency}`,
        backgroundColor: 'rgba(54, 162, 235, 0.5)',
        borderColor: 'rgb(54, 162, 235)',
        data: []
    }]
};
let currentRate = 0;
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('rateChart').getContext('2d');
    rateChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    ticks: {
                        autoSkip: true,
                        maxRotation: 0,
                        minRotation: 0,
                        color: 'white'
                    },

                },
                y: {
                    beginAtZero: false,
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
});

function updateChart(price, time) {
    chartData.labels.push(time);
    chartData.datasets[0].data.push(price);
    rateChart.update();

    if (chartData.labels.length > 60) {
        chartData.labels.shift();
        chartData.datasets[0].data.shift();
    }
}

const apiKey = '8f5501d6db23484127f4bb1ef51605785bd4fd9248dd0827715933a72ff5a729';
let ws = new WebSocket(`wss://streamer.cryptocompare.com/v2?api_key=${apiKey}`);
ws.onmessage = function (event) {
    const response = JSON.parse(event.data);
    if (response.TYPE === "5" && response.PRICE) {
        currentRate = response.PRICE;
        document.getElementById('currentRate').innerText = currentRate;
        document.getElementById('currentRate').style.color = 'white';
        calculate();
        // 获取当前时间
        const now = new Date();
        // 格式化时间为 'YYYY-MM-DD HH:mm' 的格式
        const year = now.getFullYear();
        const month = ('0' + (now.getMonth() + 1)).slice(-2); // 月份从0开始，所以加1
        const day = ('0' + now.getDate()).slice(-2);
        const hours = ('0' + now.getHours()).slice(-2);
        const minutes = ('0' + now.getMinutes()).slice(-2);
        const seconds = ('0' + now.getSeconds()).slice(-2);
        const formattedTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds} |`;
        // 更新实时汇率显示
        document.getElementById('currentRate').innerText = response.PRICE;
        // 更新图表
        updateChart(response.PRICE, formattedTime);
    }
};


ws.onopen = function () {
    const msg = JSON.stringify({
        "action": "SubAdd",
        "subs": [`5~CCCAGG~${fromCurrency}~${toCurrency}`]
    });
    ws.send(msg);
};


ws.onerror = function (error) {
    console.error('WebSocket Error:', error);
};
ws.onclose = function (event) {

    console.log('WebSocket connection closed: ', event);

    setTimeout(function () {
        ws = new WebSocket(`wss://streamer.cryptocompare.com/v2?api_key=${apiKey}`);
    }, 5000);
};

function calculate() {

    const amountElement = document.getElementById('amount');
    const amount = amountElement.value;

    if (amount !== '' && currentRate) {
        const result = (amount * currentRate);

        document.getElementById('result').innerText = `${result} ${toCurrency}`;
    } else {

        document.getElementById('result').innerText = `NaN ${toCurrency}`;
    }
}