//sd_kline_chart.js

document.addEventListener('DOMContentLoaded', () => {
    // 按钮点击事件处理
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const days = this.getAttribute('data-value');
            if (stockCode) {
                fetchKLineData(stockCode, days);
            } else {
                console.error('股票代码尚未设置');
            }
        });
    });

    // 显示时间范围选项
    document.getElementById('btn-kline').addEventListener('click', function() {
        document.getElementById('date-range-options').style.display = 'block';
    });
});

function fetchKLineData(stockCode, kLineRange) {
    const url = `/mc/k_line_data?stock_code=${encodeURIComponent(stockCode)}&k_line_ranges=${encodeURIComponent(kLineRange || 'max')}`;
    console.log('Fetching data from:', url); // 添加此行以调试 URL
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Received data:', data); // 添加此行以调试数据
            if (data.k_line_data) {
                generateKLineChart(data.k_line_data);
            } else {
                console.error('No K-Line data found in response');
            }
        })
        .catch(error => console.error('Error fetching K-Line data:', error));
}



function generateKLineChart(kLineData) {
    if (!Array.isArray(kLineData) || kLineData.length === 0) {
        console.error('Invalid K-Line Data');
        return;
    }

    const trace = {
        x: kLineData.map(record => new Date(record['Date'])),
        open: kLineData.map(record => record['Open']),
        high: kLineData.map(record => record['High']),
        low: kLineData.map(record => record['Low']),
        close: kLineData.map(record => record['Close']),
        type: 'candlestick',
        name: 'K线图'
    };

    const layout = {
        title: 'K线图',
        xaxis: { title: '日期', type: 'date', tickformat: '%Y-%m-%d' },
        yaxis: { title: '价格' }
    };

    const chartContainerId = 'kline-chart';
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer) {
        Plotly.purge(chartContainerId);  // 清除旧图表
        Plotly.newPlot(chartContainerId, [trace], layout); // 重新绘制图表
    } else {
        console.error('Chart container not found');
    }
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const stockCode = getQueryParam('stock_code') || '';
console.log(stockCode);