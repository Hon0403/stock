# 股票資訊系統 (Stock Information System)

這是一個使用 Python Flask 框架開發的網頁應用程式，旨在提供使用者查詢台灣股市相關資訊、市場新聞公告以及個股分析工具。 此專案整合了多個公開資料來源，提供一個集中化的資訊平台，適合**展示**全端開發能力。

## 系統畫面展示

### 登入畫面
![登入畫面](./images/login_screenshot.png)  
*系統登入介面，**說明**使用 Flask-Login 和 bcrypt 提供安全的用戶認證。*

### 首頁儀表板 (範例)
![首頁儀表板](./images/dashboard_screenshot.png)  
*登入後的主畫面，**展示**整合的市場概況、新聞公告及個股查詢入口。*

### 個股資訊頁面 (範例)
![個股概況](./images/stock_info_screenshot.png)  
*查詢個股後的詳細資訊頁面，包含基本資料、報價與 K 線圖。*

### K 線圖互動 (範例)
![技術分析](./images/kline_chart_screenshot.png)  
*互動式 K 線圖，**演示**切換不同時間區間的功能。*

*(請務必將 `images/` 後面的檔名換成你實際的截圖檔名，並確保圖片已上傳到 GitHub 的 `images` 資料夾)*

## 主要功能 (Key Features)

*   **用戶認證系統 (User Authentication):**
    *   提供安全的登入與登出機制 (**提及**使用 **Flask-Login** 進行會話管理)。
    *   使用 **bcrypt** 對使用者密碼進行安全的雜湊加密儲存 (**強調**安全性)。
*   **個股資訊查詢 (Stock Information Query):**
    *   **展示**如何查詢並顯示上市/上櫃/興櫃公司基本資料 (董事長、總經理等)。
    *   **展示**即時與歷史交易資訊 (開盤、收盤、最高、最低、成交量等，**說明**資料來自 **Yahoo Finance** / **TWSE API**)。
*   **互動式 K 線圖 (Interactive K-Line Charts):**
    *   **演示**如何視覺化呈現股票歷史價格走勢。
    *   **演示**支援不同時間區間（日、週、月）的數據查詢與顯示 (**點擊切換**區間)。
    *   使用 **[請務必填寫 ECharts 或 Highcharts]** 實現豐富的圖表互動。
*   **市場新聞與公告 (Market News & Announcements):**
    *   **展示**即時獲取並顯示**台灣證券交易所 (TWSE)** 發布的重大訊息、臨時公告等。
    *   **整合**加權指數等市場概況資訊，方便掌握市場動態。
*   **多重資料來源整合 (Multi-Source Data Integration):**
    *   **台灣證券交易所 (TWSE):** 透過官方 API 獲取新聞、公告。
    *   **Yahoo Finance:** 利用 `yfinance` 套件獲取個股歷史股價及數據。
    *   **櫃檯買賣中心 (TPEx):** **說明**因無 API，故使用網頁爬蟲 (**Selenium** + **BeautifulSoup4**) 獲取股票代碼。
    *   **提及**實現了簡單的 `is_data_up_to_date` 資料更新檢查機制。
*   **響應式網頁設計 (Responsive Web Design):**
    *   使用 **Bootstrap 5** 框架，**說明**確保在不同尺寸裝置上的瀏覽體驗。

## 技術棧 (Technology Stack)
*(這部分本身就是很好的技術關鍵字小抄)*
此專案採用了現代化的 Web 開發技術組合，旨在實現功能完整、易於維護且具備良好使用者體驗的目標。

*   **後端 (Backend):**
    *   **Python 3.11:** 主要開發語言。
    *   **Flask:** 輕量級 WSGI Web 框架 (**說明**選擇原因：靈活、快速開發)。
    *   **SQLAlchemy:** 強大的 ORM (**說明**簡化資料庫操作)。
    *   **Flask-Login:** 處理使用者認證與會話管理。
    *   **Flask-WTF:** 處理網頁表單、驗證與 **CSRF 保護**。
    *   **Requests:** 發送 HTTP 請求，與外部 API 互動。
    *   **Selenium & BeautifulSoup4:** **說明**用於網頁爬蟲，抓取無 API 的資料。
    *   **Bcrypt:** 用於密碼雜湊，提升安全性。
*   **前端 (Frontend):**
    *   **HTML5:** 網頁結構。
    *   **CSS3:** 網頁樣式 (**Bootstrap 5** 輔助)。
    *   **JavaScript (ES6+):** 實現前端互動邏輯。
    *   **jQuery:** 簡化 DOM 操作和事件處理。
    *   **[請務必填寫 ECharts 或 Highcharts]:** 強大的圖表庫，**說明**用於視覺化 K 線圖。
    *   **AJAX/Fetch API:** **說明**用於非同步請求，提升使用者體驗 (如動態載入圖表數據)。
*   **資料庫 (Database):**
    *   **SQL Server:** 關係型資料庫 (**說明**用於儲存使用者帳號)。
*   **開發工具與環境 (Development Tools & Environment):**
    *   **Git:** 版本控制。
    *   **Virtual Environment (`venv`):** 環境隔離。
    *   **IDE:** Visual Studio Code。

## 系統架構 (System Architecture)
*(這部分也是很好的架構關鍵字小抄)*
*   採用 **Flask Blueprint** 組織路由與視圖 (**說明**模組化開發)。
*   遵循 **關注點分離** 原則 (類似 MVC/MVVM)，分離資料、邏輯與介面。
*   前後端主要透過 **AJAX/Fetch API** 請求 + **Jinja2** 模板渲染進行交互。 (**提及**可能有 FastAPI 的 RESTful API 部分)。
*   透過 `config.py` 集中管理配置，建議透過 **環境變數** 加載敏感資訊。
*   使用 `exts.py` 統一管理 Flask 擴充套件實例。

## 資料來源 (Data Sources)
*(可以稍微提一下整合不同來源的挑戰)*
*   **台灣證券交易所 (TWSE)** 開放 API
*   **Yahoo Finance API** (透過 `yfinance`)
*   **櫃檯買賣中心 (TPEx)** 網站 (爬蟲)

## 如何運行 (How to Run)
*(這部分主要是給別人看，Demo 時不太會唸)*
1.  **克隆儲存庫:**
    ```
    git clone https://github.com/Hon0403/stock.git
    cd stock
    ```
2.  **建立並啟動虛擬環境:**
    ```
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **安裝所需的 Python 套件:**
    ```
    python -m pip install -r requirements.txt
    ```
    *(確保 `requirements.txt` 是最新的)*
4.  **(若使用 Selenium) 安裝 ChromeDriver:** 確保已安裝匹配的 ChromeDriver 或使用 `webdriver-manager`。
5.  **設定環境變數:** 參考 `config.py` 設定 `DATABASE_URL`, `SECRET_KEY` 等。
6.  **(可選) 初始化資料庫/運行爬蟲。**
7.  **運行 Flask 應用程式:**
    ```
    python -m flask run
    # 或 python app.py
    ```
8.  開啟 `http://127.0.0.1:5000`。

## 測試帳號 (Test Account)
*(Demo 登入時用)*
為方便評估系統功能，可使用以下測試帳號登入：

*   **帳號：** `12`
*   **密碼：** `12`

*注意：此為測試帳號。*

## 目前未完成/規劃中功能
*(Demo 結尾時提及未來展望)*
*   **說明**漲跌停資訊*尚未整合完成*。
*   **提及**規劃加入 MACD/RSI 指標。
*   **提到**可進一步優化行動裝置介面。
*   **說明**尚未實作「忘記密碼」/「註冊」。
*   **提到**可加入 Redis 快取優化效能。
*   **提及**可完善錯誤處理與日誌。

