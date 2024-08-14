//sd_kline_chart.js

document.addEventListener('DOMContentLoaded', () => {
    const stockCode = getQueryParam('stock_code') || '';
    console.log(stockCode);

    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const days = this.getAttribute('data-value');
            console.log('Selected data-value:', days);

            if (this.id === 'btn-kline') {
                showDateRangeOptions();
            }
            if (stockCode) {
                fetchKLineData(stockCode, days);
            } else {
                console.error('股票代碼尚未設置');
            }
        });
    });

    document.getElementById('btn-kline').addEventListener('click', showDateRangeOptions);
});

function showDateRangeOptions() {
    document.getElementById('date-range-options').style.display = 'block';
}

function fetchKLineData(stockCode, kLineRange) {
    const url = `/mc/k_line_data?stock_code=${encodeURIComponent(stockCode)}&k_line_ranges=${encodeURIComponent(kLineRange || 'max')}`;
    console.log('從以下地址獲取數據:', url);

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP錯誤！狀態碼: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('接收到的數據:', data);
            if (data.k_line_data) {
                clearChart();
                generateKLineChart(data.k_line_data, kLineRange);
            } else {
                console.error('響應中未找到K線數據');
            }
        })
        .catch(error => console.error('獲取K線數據時出錯:', error));
}

function clearChart() {
    const displayArea = document.getElementById('display-area');
    if (displayArea) {
        displayArea.innerHTML = '<div id="kline-chart"></div>';
    } else {
        console.error('未找到顯示區域');
    }

    const chartContainerId = 'kline-chart';
    if (document.getElementById(chartContainerId)) {
        Plotly.purge(chartContainerId);
    } else {
        console.error('未找到圖表容器');
    }
}

// 處理分鐘
function generateMinuteKLineChart(kLineData) {
    const candlestickTrace = createTrace(kLineData, 'Datetime');
    const lineTrace = createLineTrace(kLineData, 'Datetime');

    const layout = createLayout('%Y-%m-%d %H:%M');
    renderChart([candlestickTrace, lineTrace], layout);
}

// 處理日線
function generateDayKLineChart(kLineData, days) {
    const dateField = (days === '1h') ? 'Datetime' : 'Date';
    const candlestickTrace = createTrace(kLineData, dateField);
    const lineTrace = createLineTrace(kLineData, dateField);

    const layout = createLayout((days === '1h') ? '%Y-%m-%d %H:%M' : '%Y-%m-%d');
    renderChart([candlestickTrace, lineTrace], layout);
}

function generateKLineChart(kLineData, days) {
    if (!Array.isArray(kLineData) || kLineData.length === 0) {
        console.error('K線資料無效');
        return;
    }

    if (['1m', '2m', '5m', '15m', '30m', '60m', '90m'].includes(days)) {
        generateMinuteKLineChart(kLineData);
    } else if (['1h', '1d', '5d', '1wk', '1mo', '3mo'].includes(days)) {
        generateDayKLineChart(kLineData, days);
    } else {
        console.error('無效的時間間隔');
    }
}

function createTrace(kLineData, dateField) {
    return {
        x: kLineData.map(record => new Date(record[dateField])),
        open: kLineData.map(record => record['Open']),
        high: kLineData.map(record => record['High']),
        low: kLineData.map(record => record['Low']),
        close: kLineData.map(record => record['Close']),
        type: 'candlestick',
        name: 'K線圖',
        hovertemplate: `
        <b>日期</b>: %{x}<br>
        <b>開盤價</b>: %{open}<br>
        <b>最高價</b>: %{high}<br>
        <b>最低價</b>: %{low}<br>
        <b>收盤價</b>: %{close}<br>
        <extra></extra>
        `
    };
}

function createLineTrace(kLineData, dateField) {
    return {
        x: kLineData.map(record => new Date(record[dateField])),
        y: kLineData.map(record => record['Close']),
        type: 'scatter',
        mode: 'lines',
        name: '收盤價折線圖',
        line: { color: 'blue' },
        hovertemplate: `
        <b>日期</b>: %{x}<br>
        <b>收盤價</b>: %{y}<br>
        <extra></extra>
        `
    };
}

function createLayout(tickFormat) {
    return {
        title: 'K線圖',
        xaxis: { title: '日期', type: 'date', tickformat: tickFormat },
        yaxis: { title: '價格' }
    };
}

function renderChart(traces, layout) {
    const chartContainerId = 'kline-chart';
    const chartContainer = document.getElementById(chartContainerId);

    if (chartContainer) {
        Plotly.react(chartContainerId, traces, layout);
    } else {
        console.error('未找到圖表容器');
    }
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
