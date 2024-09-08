// utils.js

export function showDateRangeOptions() {
    const dateRangeOptions = document.getElementById('date-range-options');
    if (dateRangeOptions) {
        dateRangeOptions.style.display = 'block';
    } else {
        console.error('未找到日期範圍選項元素');
    }
}

export function hideDateRangeOptions() {
    const dateRangeOptions = document.getElementById('date-range-options');
    if (dateRangeOptions) {
        dateRangeOptions.style.display = 'none';
    } else {
        console.error('未找到日期範圍選項元素');
    }
}

export function clearOtherButtons() {
    document.querySelectorAll('.button-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
}

export function clearChart() {
    const displayArea = document.getElementById('display-area');
    if (displayArea) {
        displayArea.innerHTML = '<div id="kline-chart"></div>';
    } else {
        console.error('未找到顯示區域');
    }
}

export function generateKLineChart(kLineData) {
    if (!Array.isArray(kLineData) || kLineData.length === 0) {
        console.error('K線資料無效或為空');
        return;
    }

    console.log('原始資料:', kLineData);

    const ohlc = kLineData.map(record => {
        const date = new Date(record[0]).getTime();
        const open = parseFloat(record[1]);
        const high = parseFloat(record[2]);
        const low = parseFloat(record[3]);
        const close = parseFloat(record[4]);

        if (isNaN(date) || isNaN(open) || isNaN(high) || isNaN(low) || isNaN(close)) {
            console.error('資料格式錯誤:', record);
            return [NaN, NaN, NaN, NaN, NaN];
        }

        return [date, open, high, low, close];
    });

    console.log('格式化後的資料:', ohlc);

    Highcharts.setOptions({
        lang: {
            months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
            shortMonths: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
            weekdays: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            rangeSelectorFrom: '從',
            rangeSelectorTo: '到',
            rangeSelectorZoom: '篩選',
            loading: '載入中...',
            noData: '沒有數據',
            resetZoom: '重置縮放',
            resetZoomTitle: '重置縮放比例',
            thousandsSep: ',',
            decimalPoint: '.',
            printChart: '列印圖表',
            downloadPNG: '下載 PNG 圖片',
            downloadJPEG: '下載 JPEG 圖片',
            downloadPDF: '下載 PDF 文件',
            downloadSVG: '下載 SVG 矢量圖',
            contextButtonTitle: '導出圖表'
        }
    });
    
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
            },
            buttons: [{
                type: 'month',
                count: 1,
                text: '1月'
            }, {
                type: 'month',
                count: 3,
                text: '3月'
            }, {
                type: 'month',
                count: 6,
                text: '6月'
            }, {
                type: 'ytd',
                text: '今年'
            }, {
                type: 'year',
                count: 1,
                text: '1年'
            }, {
                type: 'all',
                text: '全部'
            }]
        },
        title: {
            text: 'K線圖'
        },
        series: [{
            type: 'candlestick',
            name: 'K線圖',
            data: ohlc,
            gapSize: 1, // 設置 gapSize 屬性
            tooltip: {
                shared: true, // 確保 tooltip 是共享的
                formatter: function () {
                    const points = this.points;
                    let tooltipHtml = '';
                    points.forEach(point => {
                        const change = Math.floor((point.point.close - point.point.open) / point.point.open * 100);
                        const changeSign = change > 0 ? '+' : '';
                        tooltipHtml += `<span style="color:${point.color}">\u25CF</span> ${point.series.name}: <b>${Math.floor(point.point.close)}</b><br/>
                                        開盤價: <b>${Math.floor(point.point.open)}</b><br/>
                                        最高價: <b>${Math.floor(point.point.high)}</b><br/>
                                        最低價: <b>${Math.floor(point.point.low)}</b><br/>
                                        收盤價: <b>${Math.floor(point.point.close)}</b><br/>
                                        漲跌: <b>${changeSign}${change}%</b><br/>`;
                    });
                    return tooltipHtml;
                }
            },
            color: 'green', // 跌的顏色
            upColor: 'red'  // 漲的顏色
        }],
        xAxis: {
            type: 'datetime',
            labels: {
                formatter: function () {
                    return Highcharts.dateFormat('%Y-%m-%d', this.value);
                }
            },
            crosshair: {
                color: 'gray',
                dashStyle: 'solid',
                label: {
                    enabled: false // 禁用 crosshair label
                }
            }
        },
        yAxis: {
            title: {
                text: '價格'
            }
        },
        credits: {
            enabled: false
        }
    });
    
    
    
    
}





