// sd_company_info.js

export function initCompanyInfo() {
    function initialize() {
        document.getElementById('btn-info').addEventListener('click', function() {
            const displayArea = document.getElementById('display-area');
            const listedinfo = document.getElementById('listed-info-json') ? document.getElementById('listed-info-json').textContent : '{}';

            try {
                const stockData = JSON.parse(listedinfo);

                displayArea.innerHTML = `
                    <h3>公司基本資訊</h3>
                    <table class="table table-striped">
                        <tbody>
                            <tr><th>出表日期</th><td>${stockData['出表日期'] || 'N/A'}</td></tr>
                            <tr><th>公司代號</th><td>${stockData['公司代號'] || 'N/A'}</td></tr>
                            <tr><th>公司名稱</th><td>${stockData['公司名稱'] || 'N/A'}</td></tr>
                            <tr><th>公司簡稱</th><td>${stockData['公司簡稱'] || 'N/A'}</td></tr>
                            <tr><th>外國企業註冊地國</th><td>${stockData['外國企業註冊地國'] || 'N/A'}</td></tr>
                            <tr><th>產業別</th><td>${stockData['產業別'] || 'N/A'}</td></tr>
                            <tr><th>住址</th><td>${stockData['住址'] || 'N/A'}</td></tr>
                            <tr><th>營利事業統一編號</th><td>${stockData['營利事業統一編號'] || 'N/A'}</td></tr>
                            <tr><th>董事長</th><td>${stockData['董事長'] || 'N/A'}</td></tr>
                            <tr><th>總經理</th><td>${stockData['總經理'] || 'N/A'}</td></tr>
                            <tr><th>發言人</th><td>${stockData['發言人'] || 'N/A'}</td></tr>
                            <tr><th>發言人職稱</th><td>${stockData['發言人職稱'] || 'N/A'}</td></tr>
                            <tr><th>代理發言人</th><td>${stockData['代理發言人'] || 'N/A'}</td></tr>
                            <tr><th>總機電話</th><td>${stockData['總機電話'] || 'N/A'}</td></tr>
                            <tr><th>成立日期</th><td>${stockData['成立日期'] || 'N/A'}</td></tr>
                            <tr><th>上市日期</th><td>${stockData['上市日期'] || 'N/A'}</td></tr>
                            <tr><th>普通股每股面額</th><td>${stockData['普通股每股面額'] || 'N/A'}</td></tr>
                            <tr><th>實收資本額</th><td>${stockData['實收資本額'] || 'N/A'}</td></tr>
                            <tr><th>私募股數</th><td>${stockData['私募股數'] || 'N/A'}</td></tr>
                            <tr><th>特別股</th><td>${stockData['特別股'] || 'N/A'}</td></tr>
                            <tr><th>編制財務報表類型</th><td>${stockData['編制財務報表類型'] || 'N/A'}</td></tr>
                            <tr><th>股票過戶機構</th><td>${stockData['股票過戶機構'] || 'N/A'}</td></tr>
                            <tr><th>過戶電話</th><td>${stockData['過戶電話'] || 'N/A'}</td></tr>
                            <tr><th>過戶地址</th><td>${stockData['過戶地址'] || 'N/A'}</td></tr>
                            <tr><th>簽證會計師事務所</th><td>${stockData['簽證會計師事務所'] || 'N/A'}</td></tr>
                            <tr><th>簽證會計師1</th><td>${stockData['簽證會計師1'] || 'N/A'}</td></tr>
                            <tr><th>簽證會計師2</th><td>${stockData['簽證會計師2'] || 'N/A'}</td></tr>
                            <tr><th>英文簡稱</th><td>${stockData['英文簡稱'] || 'N/A'}</td></tr>
                            <tr><th>英文通訊地址</th><td>${stockData['英文通訊地址'] || 'N/A'}</td></tr>
                            <tr><th>傳真機號碼</th><td>${stockData['傳真機號碼'] || 'N/A'}</td></tr>
                            <tr><th>電子郵件信箱</th><td>${stockData['電子郵件信箱'] || 'N/A'}</td></tr>
                            <tr><th>網址</th><td>${stockData['網址'] || 'N/A'}</td></tr>
                            <tr><th>已發行普通股數或TDR原股發行股數</th><td>${stockData['已發行普通股數或TDR原股發行股數'] || 'N/A'}</td></tr>
                        </tbody>
                    </table>
                `;
            } catch (error) {
                console.error('JSON parse error:', error);
                displayArea.innerHTML = '<p>資料加載錯誤。</p>';
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initialize();
        });
    } else {
        initialize();
    }
}
