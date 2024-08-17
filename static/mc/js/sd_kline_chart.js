//sd_kline_chart.js

document.addEventListener('DOMContentLoaded', () => {
    const stockCode = getQueryParam('stock_code') || '';
    console.log(stockCode);

    document.querySelectorAll('.button-group .btn').forEach(btn => {
        btn.addEventListener('click', function () {
            if (this.id === 'btn-kline') {
                clearOtherButtons();
                clearChart();
                showDateRangeOptions();
            } else {
                document.getElementById('date-range-options').style.display = 'none';
            }
        });
    });

    document.querySelectorAll('#date-range-options .btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const days = this.getAttribute('data-value');
            console.log('Selected data-value:', days);

            if (stockCode) {
                fetchKLineData(stockCode, days);
            } else {
                console.error('股票代碼尚未設置');
            }
        });
    });
});

function showDateRangeOptions() {
    document.getElementById('date-range-options').style.display = 'block';
}

function clearOtherButtons() {
    document.querySelectorAll('.button-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
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
}

function generateKLineChart(kLineData, days) {
    if (!Array.isArray(kLineData) || kLineData.length === 0) {
        console.error('K線資料無效');
        return;
    }

    const ohlc = kLineData.map(record => [
        new Date(record.Date || record.Datetime).getTime(),
        record.Open,
        record.High,
        record.Low,
        record.Close
    ]);

    Highcharts.stockChart('kline-chart', {
        accessibility: {
            enabled: false
        },
        rangeSelector: {
            selected: 1,
            inputDateFormat: '%Y年%m月%d日', // 自定義日期格式
            inputEditDateFormat: '%Y年%m月%d日', // 自定義編輯日期格式
            inputBoxWidth: 120,
            inputBoxHeight: 18,
            inputStyle: {
                color: '#039',
                fontWeight: 'bold'
            },
            labelStyle: {
                color: 'silver',
                fontWeight: 'bold'
            }
        },
        title: {
            text: 'K線圖'
        },
        series: [{
            type: 'candlestick',
            name: 'K線圖',
            data: ohlc,
            tooltip: {
                valueDecimals: 0, // 設置小數位數為0
                formatter: function () {
                    const point = this.points[0].point;
                    const change = Math.floor((point.close - point.open) / point.open * 100);
                    const changeSign = change > 0 ? '+' : '';
                    return `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: <b>${Math.floor(point.close)}</b><br/>
                            開盤價: <b>${Math.floor(point.open)}</b><br/>
                            最高價: <b>${Math.floor(point.high)}</b><br/>
                            最低價: <b>${Math.floor(point.low)}</b><br/>
                            收盤價: <b>${Math.floor(point.close)}</b><br/>
                            漲跌: <b>${changeSign}${change}%</b><br/>`;
                }
            },
            color: 'green', // 跌的顏色
            upColor: 'red'  // 漲的顏色
        }],
        xAxis: {
            type: 'datetime',
            labels: {
                enabled: false // 禁用 x 軸上的日期標籤
            },
            crosshair: {
                color: 'gray',
                dashStyle: 'solid',
                label: {
                    enabled: false // 禁用 crosshair label
                }
            }
        },
        tooltip: {
            shared: true, // 確保 tooltip 是共享的
            xDateFormat: null, // 隱藏日期
            formatter: function () {
                const points = this.points;
                let tooltipHtml = '';
                points.forEach(point => {
                    const change = Math.floor((point.point.close - point.point.open) / point.point.open * 100);
                    const changeSign = change > 0 ? '+' : '';
                    const date = Highcharts.dateFormat('%Y-%m-%d', point.point.x);
                    tooltipHtml += `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: <b>${Math.floor(point.point.close)}</b><br/>
                                    開盤價: <b>${Math.floor(point.point.open)}</b><br/>
                                    最高價: <b>${Math.floor(point.point.high)}</b><br/>
                                    最低價: <b>${Math.floor(point.point.low)}</b><br/>
                                    收盤價: <b>${Math.floor(point.point.close)}</b><br/>
                                    漲跌: <b>${changeSign}${change}%</b><br/>
                                    日期: <b>${date}</b><br/>`;
;
                });
                return tooltipHtml;
            }
        }
    });
}










function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}
