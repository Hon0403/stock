// weighted_index.js

fetch('/mc/api/weighted_index')
    .then(response => response.json())
    .then(data => {
        console.log('API 返回數據:', data); // 確保數據格式正確

        if (data.length > 0) {
            // 取得最新和昨天的數據
            const latestData = data[data.length - 1];
            const previousData = data[data.length - 2] || latestData;

            // 更新最新收盤價
            document.getElementById('last-price').textContent = latestData.Close.toFixed(2);

            // 計算變化量和變化率
            let change = latestData.Close - previousData.Close;
            let changeRate = ((change / previousData.Close) * 100).toFixed(2);

            // 設置變化量和變化率的顏色
            let changeElement = document.getElementById('change');
            let changeRateElement = document.getElementById('changeRate');

            if (change >= 0) {
                changeElement.classList.add('up');
                changeElement.classList.remove('down');
                changeRateElement.classList.add('up');
                changeRateElement.classList.remove('down');
            } else {
                changeElement.classList.add('down');
                changeElement.classList.remove('up');
                changeRateElement.classList.add('down');
                changeRateElement.classList.remove('up');
            }

            // 更新變化量和變化率
            changeElement.textContent = change.toFixed(2);
            changeRateElement.textContent = changeRate + '%';
        } else {
            // 無數據時顯示
            document.getElementById('last-price').textContent = '無資料';
            document.getElementById('change').textContent = '--';
            document.getElementById('changeRate').textContent = '--';
        }
    })
    .catch(error => {
        console.error('Error fetching weighted index data:', error);
    });
