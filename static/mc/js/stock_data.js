// 優化版的 stock_data.js

document.addEventListener('DOMContentLoaded', () => {
    // 獲取按鈕和顯示區域
    const btnInfo = document.getElementById('btn-info');
    const btnTrading = document.getElementById('btn-trading');
    const btnKline = document.getElementById('btn-kline');
    const displayArea = document.getElementById('display-area');

    // 初始化全局數據
    const STOCK_DATA_GLOBAL = {
        stockData: JSON.parse(document.getElementById('stock-data-json').textContent || '{}'),
        stockInfo: JSON.parse(document.getElementById('stock-info-json').textContent || '{}'),
        kLineData: JSON.parse(document.getElementById('k-line-data-json')?.textContent || '[]').map(d => ({
            date: d.date,
            open: d.Open,
            high: d.High,
            low: d.Low,
            close: d.Close,
            volume: d.Volume
        }))
    };

    // 綁定按鈕事件
    btnInfo.addEventListener('click', () => displayCompanyInfo(STOCK_DATA_GLOBAL, displayArea));
    btnTrading.addEventListener('click', () => displayTradingInfo(STOCK_DATA_GLOBAL, displayArea));
    btnKline.addEventListener('click', () => displayKLineChart(STOCK_DATA_GLOBAL, displayArea));
});

// 驗證K線圖數據
function validateKLineData(data) {
    return data.filter(d => !isNaN(new Date(d.date)) && !isNaN(d.open) && !isNaN(d.high) && !isNaN(d.low) && !isNaN(d.close));
}

// 顯示公司基本資訊
function displayCompanyInfo(globalData, displayArea) {
    const { stockData, stockInfo } = globalData;
    displayArea.innerHTML = `
        <h3>公司基本資訊</h3>
        <table class="table table-striped">
            <tbody>
                <tr><th>股票代碼</th><td>${stockData.code || 'N/A'}</td></tr>
                <tr><th>股票名稱</th><td>${stockData.name || 'N/A'}</td></tr>
                <tr><th>價格</th><td>${stockData.price || 'N/A'}</td></tr>
                <tr><th>漲跌</th><td>${stockData.change || 'N/A'}</td></tr>
                <tr><th>漲跌百分比</th><td>${stockData.changePercent || 'N/A'}</td></tr>
                <tr><th>成交量</th><td>${stockData.volume || 'N/A'}</td></tr>
                <tr><th>開盤價</th><td>${stockData.open || 'N/A'}</td></tr>
                <tr><th>收盤價</th><td>${stockData.close || 'N/A'}</td></tr>
                <tr><th>最高價</th><td>${stockData.high || 'N/A'}</td></tr>
                <tr><th>最低價</th><td>${stockData.low || 'N/A'}</td></tr>
                <tr><th>所屬產業</th><td>${stockInfo.sector || 'N/A'}</td></tr>
                <tr><th>行業</th><td>${stockInfo.industry || 'N/A'}</td></tr>
                <tr><th>國家</th><td>${stockInfo.country || 'N/A'}</td></tr>
                <tr><th>員工數量</th><td>${stockInfo.employees || 'N/A'}</td></tr>
                <tr><th>CEO</th><td>${stockInfo.ceo || 'N/A'}</td></tr>
                <tr><th>最後更新時間</th><td>${stockData.last_modified || 'N/A'}</td></tr>
            </tbody>
        </table>
    `;
}

// 顯示交易資訊
function displayTradingInfo(globalData, displayArea) {
    const { stockData, stockInfo } = globalData;
    displayArea.innerHTML = `
        <h3>交易資訊</h3>
        <table class="table table-striped">
            <tbody>
                <tr><th>開盤價</th><td>${stockInfo.regularMarketOpen || 'N/A'}</td></tr>
                <tr><th>收盤價</th><td>${stockInfo.regularMarketPreviousClose || 'N/A'}</td></tr>
                <tr><th>最高價</th><td>${stockInfo.regularMarketDayHigh || 'N/A'}</td></tr>
                <tr><th>最低價</th><td>${stockInfo.regularMarketDayLow || 'N/A'}</td></tr>
                <tr><th>成交量</th><td>${stockData.volume || 'N/A'}</td></tr>
                <tr><th>成交金額</th><td>${stockData.turnover || 'N/A'}</td></tr>
                <tr><th>市值</th><td>${stockData.marketCap || 'N/A'}</td></tr>
                <tr><th>流通市值</th><td>${stockData.freeFloatMarketCap || 'N/A'}</td></tr>
                <tr><th>市盈率</th><td>${stockData.peRatio || 'N/A'}</td></tr>
                <tr><th>市淨率</th><td>${stockData.pbRatio || 'N/A'}</td></tr>
                <tr><th>換手率</th><td>${stockData.turnoverRate || 'N/A'}</td></tr>
            </tbody>
        </table>
    `;
}

// 顯示K線圖
function displayKLineChart(globalData, displayArea) {
    displayArea.innerHTML = `
        <h3>K線圖</h3>
        <svg id="kline-chart" width="100%" height="400"></svg>
    `;

    const kLineData = globalData.kLineData;

    // 確保數據是正確的
    if (!kLineData || kLineData.length === 0) {
        displayArea.innerHTML = '<p>沒有 K 線圖數據可顯示。</p>';
        return;
    }
 
    // 日期格式解析
    const parseDate = d3.timeParse('%Y-%m-%d');  // 解析日期格式

    // 將日期字符串轉換為日期對象
    const formattedData = kLineData.map(d => ({
        ...d,
        date: parseDate(d.date)  // 確保將日期字符串轉換為日期對象
    }));

    const svg = d3.select('#kline-chart');
    const margin = { top: 20, right: 20, bottom: 30, left: 50 };
    const width = svg.node().getBoundingClientRect().width - margin.left - margin.right;
    const height = svg.node().getBoundingClientRect().height - margin.top - margin.bottom;

    const x = d3.scaleTime().range([0, width]);
    const y = d3.scaleLinear().range([height, 0]);

    const xAxis = d3.axisBottom().scale(x);
    const yAxis = d3.axisLeft().scale(y);

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', `translate(${margin.left},${height + margin.top})`)
        .call(xAxis);

    svg.append('g')
        .attr('class', 'y axis')
        .attr('transform', `translate(${margin.left},${margin.top})`)
        .call(yAxis);

    // 設置 x 軸和 y 軸的域
    x.domain(d3.extent(formattedData, d => d.date));
    y.domain([
        d3.min(formattedData, d => Math.min(d.open, d.close)),
        d3.max(formattedData, d => Math.max(d.open, d.close))
    ]);

    svg.selectAll('.line')
        .data(formattedData)
        .enter().append('line')
        .attr('x1', d => x(d.date))
        .attr('x2', d => x(d.date))
        .attr('y1', d => y(Math.max(d.open, d.close)))
        .attr('y2', d => y(Math.min(d.open, d.close)))
        .attr('stroke', d => d.open > d.close ? 'red' : 'green')
        .attr('stroke-width', 2)
        .attr('transform', `translate(${margin.left},${margin.top})`);

    svg.selectAll('.bar')
        .data(formattedData)
        .enter().append('rect')
        .attr('x', d => x(d.date) - 5)
        .attr('y', d => y(Math.max(d.open, d.close)))
        .attr('width', 10)
        .attr('height', d => Math.abs(y(d.open) - y(d.close)))
        .attr('fill', d => d.open > d.close ? 'red' : 'green')
        .attr('transform', `translate(${margin.left},${margin.top})`);
}
