// sd_trading_info.js
document.addEventListener('DOMContentLoaded', () => {
    const btnTrading = document.getElementById('btn-trading');
    const displayArea = document.getElementById('display-area');

    btnTrading.addEventListener('click', () => displayTradingInfo(displayArea));
});

function displayTradingInfo(displayArea) {
    const stockData = JSON.parse(document.getElementById('stock-data-json').textContent || '{}');
    const stockInfo = JSON.parse(document.getElementById('stock-info-json').textContent || '{}');

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
