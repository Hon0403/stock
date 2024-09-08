// otc_Kline_Chart.js

import { clearChart, generateKLineChart, showDateRangeOptions, clearOtherButtons } from './utils.js';

export function initOTCKLineChart(marketCode) {
    if (!marketCode) {
        console.error('未找到 market_code');
        return;
    }

    document.querySelectorAll('.main-button-group .main-btn').forEach(btn => {
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
            fetchOTCKLineData(marketCode, days);
        });
    });
}


function fetchOTCKLineData(marketCode, days) {
    const url = `/mc/otc_k_line_data?marketCode=${encodeURIComponent(marketCode)}&days=${encodeURIComponent(days)}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP錯誤！狀態碼: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.otc_k_line_data) {
                const formattedData = data.otc_k_line_data.map(record => {
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
            
                clearChart();
                generateKLineChart(formattedData);
            } else {
            }
            
        })
        
        .catch(error => {
            console.error("Error fetching OTC K-line data:", error);
        });
}

