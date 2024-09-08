// mc/js/otcEsmData.js

export function initotcEsmData() {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initialize();
        });
    } else {
        initialize();
    }

    function initialize() {
        console.log('DOMContentLoaded event fired'); // 調試信息：確保事件觸發

        // 確保按鈕存在，然後添加事件監聽器
        const btnInfo = document.getElementById('btn-info');
        if (btnInfo) {
            console.log('Button with id "btn-info" found'); // 調試信息：確保按鈕存在

            btnInfo.addEventListener('click', function() {
                console.log('Button clicked'); // 調試信息：確保按鈕點擊事件觸發
                const displayArea = document.getElementById('display-area');
                const basicInfoScript = document.getElementById('basic-info-json');
                
                if (basicInfoScript) {
                    try {
                        const basicInfoText = basicInfoScript.textContent;
                        console.log('Basic Info Text:', basicInfoText); // 調試信息：檢查 basicInfoText 內容
                        const basicInfo = JSON.parse(basicInfoText);

                        console.log('Basic Info:', basicInfo); // 調試信息：檢查 basicInfo 內容

                        // 更新顯示區域
                        displayArea.innerHTML = `
                            <h3>公司基本資訊</h3>
                            <table class="table table-striped">
                                <tbody>
                                    <tr><th>出表日期</th><td>${basicInfo.Date || 'N/A'}</td></tr>
                                    <tr><th>公司代號</th><td>${basicInfo.SecuritiesCompanyCode || 'N/A'}</td></tr>
                                    <tr><th>公司名稱</th><td>${basicInfo.CompanyName || 'N/A'}</td></tr>
                                    <tr><th>公司簡稱</th><td>${basicInfo.CompanyAbbreviation || 'N/A'}</td></tr>
                                    <tr><th>外國企業註冊地國</th><td>${basicInfo.Registration || 'N/A'}</td></tr>
                                    <tr><th>產業別</th><td>${basicInfo.SecuritiesIndustryCode || 'N/A'}</td></tr>
                                    <tr><th>住址</th><td>${basicInfo.Address || 'N/A'}</td></tr>
                                    <tr><th>營利事業統一編號</th><td>${basicInfo["UnifiedBusinessNo."] || 'N/A'}</td></tr>
                                    <tr><th>董事長</th><td>${basicInfo.Chairman || 'N/A'}</td></tr>
                                    <tr><th>總經理</th><td>${basicInfo.GeneralManager || 'N/A'}</td></tr>
                                    <tr><th>發言人</th><td>${basicInfo.Spokesman || 'N/A'}</td></tr>
                                    <tr><th>發言人職稱</th><td>${basicInfo.TitleOfSpokesman || 'N/A'}</td></tr>
                                    <tr><th>代理發言人</th><td>${basicInfo.DeputySpokesperson || 'N/A'}</td></tr>
                                    <tr><th>總機電話</th><td>${basicInfo.Telephone || 'N/A'}</td></tr>
                                    <tr><th>成立日期</th><td>${basicInfo.DateOfIncorporation || 'N/A'}</td></tr>
                                    <tr><th>上市日期</th><td>${basicInfo.DateOfListing || 'N/A'}</td></tr>
                                    <tr><th>普通股每股面額</th><td>${basicInfo.ParValueOfCommonStock || 'N/A'}</td></tr>
                                    <tr><th>實收資本額</th><td>${basicInfo["Paidin.Capital.NTDollars"] || 'N/A'}</td></tr>
                                    <tr><th>私募股數</th><td>${basicInfo["PrivateStock.shares"] || 'N/A'}</td></tr>
                                    <tr><th>特別股</th><td>${basicInfo["PreferredStock.shares"] || 'N/A'}</td></tr>
                                    <tr><th>編制財務報表類型</th><td>${basicInfo.PreparationOfFinancialReportType || 'N/A'}</td></tr>
                                    <tr><th>股票過戶機構</th><td>${basicInfo.StockTransferAgent || 'N/A'}</td></tr>
                                    <tr><th>過戶電話</th><td>${basicInfo.StockTransferAgentTelephone || 'N/A'}</td></tr>
                                    <tr><th>過戶地址</th><td>${basicInfo.StockTransferAgentAddress || 'N/A'}</td></tr>
                                    <tr><th>簽證會計師事務所</th><td>${basicInfo.AccountingFirm || 'N/A'}</td></tr>
                                    <tr><th>簽證會計師1</th><td>${basicInfo["CPA.CharteredPublicAccountant.First"] || 'N/A'}</td></tr>
                                    <tr><th>簽證會計師2</th><td>${basicInfo["CPA.CharteredPublicAccountant.Second"] || 'N/A'}</td></tr>
                                    <tr><th>英文簡稱</th><td>${basicInfo.Symbol || 'N/A'}</td></tr>
                                    <tr><th>傳真機號碼</th><td>${basicInfo.Fax || 'N/A'}</td></tr>
                                    <tr><th>電子郵件信箱</th><td>${basicInfo.EmailAddress || 'N/A'}</td></tr>
                                    <tr><th>網址</th><td>${basicInfo.WebAddress || 'N/A'}</td></tr>
                                    <tr><th>已發行普通股數或TDR原股發行股數</th><td>${basicInfo.IssueShares || 'N/A'}</td></tr>
                                </tbody>
                            </table>
                        `;
                    } catch (error) {
                        console.error('JSON parse error:', error);
                        displayArea.innerHTML = '<p>資料加載錯誤。</p>';
                    }
                } else {
                    console.error('Basic info JSON script tag not found.');
                    displayArea.innerHTML = '<p>資料加載錯誤。</p>';
                }
            });
        } else {
            console.error('Button with id "btn-info" not found.');
        }
    }
}
