// sd_kline_Chart.js

import { clearChart, generateKLineChart, showDateRangeOptions, clearOtherButtons } from './utils.js';

export function initKLineChart(stockCode) {
    function initialize() {
        if (!stockCode) {
            console.error('股票代碼尚未設置');
            return;
        }

        document.querySelectorAll('.main-button-group .main-btn').forEach(btn => {
            btn.addEventListener('click', function () {
                if (this.id === 'btn-kline') {
                    clearOtherButtons();
                    clearChart();
                    showDateRangeOptions();
                } else {
                    hideDateRangeOptions();
                }
            });
        });

        document.querySelectorAll('#date-range-options .btn').forEach(btn => {
            btn.addEventListener('click', function () {
                const days = this.getAttribute('data-value');
                fetchKLineData(stockCode, days);
            });
        });
    }

    function hideDateRangeOptions() {
        // 你的函數邏輯
        console.log('hideDateRangeOptions 被調用了');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initialize();
        });
    } else {
        initialize();
    }
}

function fetchKLineData(stockCode, kLineRange) {
    const url = `/mc/k_line_data?stock_code=${encodeURIComponent(stockCode)}&k_line_ranges=${encodeURIComponent(kLineRange || 'max')}`;
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP錯誤！狀態碼: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.k_line_data) {
                const formattedData = formatKLineData(data.k_line_data);
                clearChart();
                generateKLineChart(formattedData, kLineRange);
            } else {
                console.error('響應中未找到K線數據');
            }
        })
        .catch(error => console.error('獲取K線數據時出錯:', error));
}

function formatKLineData(data) {
    return data.map(record => {
        const date = new Date(record.Date).getTime();
        const open = parseFloat(record.Open);
        const high = parseFloat(record.High);
        const low = parseFloat(record.Low);
        const close = parseFloat(record.Close);

        if (isNaN(date) || isNaN(open) || isNaN(high) || isNaN(low) || isNaN(close)) {
            console.error('資料格式錯誤:', record);
            return [NaN, NaN, NaN, NaN, NaN];
        }

        return [date, open, high, low, close];
    });
}
