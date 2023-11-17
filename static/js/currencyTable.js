// 定义全局变量来存储图表实例和图表数据
let rateChart;
let chartData = {
    labels: [], // X轴的标签数组
    datasets: [{
        label: 'BTC to USD',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        borderColor: 'rgb(255, 99, 132)',
        data: [] // Y轴的数据数组
    }]
};

// 当DOM完全加载后初始化图表
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('rateChart').getContext('2d');
    rateChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'linear'
                }],
                yAxes: [{
                    beginAtZero: false
                }]
            }
        }
    });
});

// 更新图表的函数
function updateChart(price, time) {
    // 添加新的数据点到图表
    chartData.labels.push(time);
    chartData.datasets[0].data.push(price);

    // 更新图表
    rateChart.update();

    // 如果图表数据点过多，删除最旧的数据点
    if (chartData.labels.length > 60) {
        chartData.labels.shift();
        chartData.datasets[0].data.shift();
    }
}
const apiKey = 'fdaacc91c4f89786b14f193e53821e1bee6f29209215ef67d6c6bf07ccfc0ddd';  // 替换为你的API密钥
// WebSocket连接和消息处理
let ws = new WebSocket(`wss://streamer.cryptocompare.com/v2?api_key=${apiKey}`);
ws.onmessage = function(event) {
    const response = JSON.parse(event.data);
    // 确保是我们订阅的汇率更新消息
    if (response.TYPE === "5" && response.PRICE) {
        // 获取当前时间
        const time = new Date();
        // 更新实时汇率显示
        document.getElementById('currentRate').innerText = response.PRICE;
        // 更新图表
        updateChart(response.PRICE, time);
    }
};


ws.onopen = function() {
    // 订阅BTC到USD的汇率数据
    const msg = JSON.stringify({
        "action": "SubAdd",
        "subs": ["5~CCCAGG~BTC~USD"]
    });
    ws.send(msg);
};


ws.onerror = function(error) {
    // 处理错误
    console.error('WebSocket Error:', error);
};

ws.onclose = function(event) {
    // 在连接关闭时处理事件，考虑重新连接
    console.log('WebSocket connection closed: ', event);
    // 等待5秒后重新连接
    setTimeout(function() {
        ws = new WebSocket(`wss://streamer.cryptocompare.com/v2?api_key=${apiKey}`);
    }, 5000);
};

// 根据需要更新图表的代码，这可能需要根据您的图表库来实现
// 如果需要定时刷新整个图表，可以在这里实现
setInterval(() => {
    // 在这里实现获取过去五分钟的汇率数据的逻辑
    // 然后调用 updateChart() 函数更新图表
    // 由于这个例子是实时更新，所以这部分可以省略
}, 3000); // 每五分钟执行一次

