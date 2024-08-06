document.addEventListener('DOMContentLoaded', () => {
    const btnInfo = document.getElementById('btn-info');
    const displayArea = document.getElementById('display-area');

    btnInfo.addEventListener('click', () => displayCompanyInfo(displayArea));
});

function displayCompanyInfo(displayArea) {
    const stockData = JSON.parse(document.getElementById('stock-data-json').textContent || '{}');
    const stockInfo = JSON.parse(document.getElementById('stock-info-json').textContent || '{}');

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
