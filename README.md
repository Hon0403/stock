# 股票資訊系統 (Stock Information System) 待更新

這是一個使用 Python Flask 框架開發的網頁應用程式，旨在提供使用者查詢台灣股市相關資訊、市場新聞公告以及個股分析工具。此專案整合了多個公開資料來源，提供一個集中化的資訊平台。

## 主要功能 (Key Features)

*   **用戶認證系統 (User Authentication):**
    *   提供安全的登入與登出機制 (使用 Flask-Login)。
    *   使用 bcrypt 進行密碼加密儲存。
*   **個股資訊查詢 (Stock Information Query):**
    *   顯示公司基本資料（如：董事長、總經理、實收資本額等）。
    *   展示即時與歷史交易資訊（開盤、收盤、最高、最低、成交量等）。
*   **互動式 K 線圖 (Interactive K-Line Charts):**
    *   視覺化呈現股票歷史價格走勢。
    *   支援不同時間區間（日、週、月）的數據查詢與顯示。
    *   使用 ECharts / Highcharts (依您實際使用的庫) 進行繪製。
*   **市場新聞與公告 (Market News & Announcements):**
    *   即時獲取並展示台灣證券交易所發布的重大訊息、臨時公告、注意處置股票等。
    *   整合加權指數等市場概況資訊。
*   **多重資料來源整合 (Multi-Source Data Integration):**
    *   **台灣證券交易所 (TWSE):** 透過官方 API 獲取新聞、公告、漲跌停資訊。
    *   **Yahoo Finance:** 獲取個股歷史股價資料。
    *   **櫃檯買賣中心 (TPEx):** 透過網頁爬蟲 (Selenium/BeautifulSoup) 獲取上櫃/興櫃股票代碼。
    *   實現資料更新檢查機制，確保資訊的時效性。
*   **響應式網頁設計 (Responsive Web Design):**
    *   使用 Bootstrap 框架，適應不同尺寸的裝置瀏覽。

## 技術棧 (Technology Stack)

*   **後端 (Backend):**
    *   Python 3.x
    *   Flask (Web 框架)
    *   SQLAlchemy (ORM, 資料庫互動)
    *   Flask-Login (使用者認證)
    *   Flask-WTF (表單處理與 CSRF 保護)
    *   Requests (HTTP 請求)
    *   Selenium, BeautifulSoup4 (網頁爬蟲)
    *   Bcrypt (密碼雜湊)
*   **前端 (Frontend):**
    *   HTML5
    *   CSS3 (包含自訂樣式與 Bootstrap 5)
    *   JavaScript (ES6+)
    *   jQuery
    *   ECharts / Highcharts (圖表庫，請確認您使用的是哪一個)
    *   AJAX/Fetch API (非同步資料請求)
*   **資料庫 (Database):**
    *   SQL Server (根據 `config.py` 設定)
*   **開發工具與環境 (Development Tools & Environment):**
    *   Git (版本控制)
    *   Virtual Environment (環境隔離)
    *   (可補充您使用的 IDE，如 VS Code)

## 系統架構 (System Architecture)

*   採用 **Flask Blueprint** 組織路由與視圖，實現模組化開發。
*   遵循類 **MVC (Model-View-Controller)** 或 **MVVM (Model-View-ViewModel)** 的設計模式，分離資料、業務邏輯與使用者介面。
*   前後端透過 **RESTful API** 或 **AJAX/Fetch** 進行資料交換。
*   設定檔 (`config.py`) 管理資料庫連線、API 金鑰等敏感資訊，並透過環境變數加載。
*   使用 `exts.py` 統一管理 Flask 擴充套件實例。

## 資料來源 (Data Sources)

*   台灣證券交易所 (TWSE) 開放 API
*   Yahoo Finance API
*   櫃檯買賣中心 (TPEx) 網站

## 如何運行 (How to Run)

1.  安裝所需的 Python 套件：`pip install -r requirements.txt` (如果有的話，或列出主要套件)
2.  設定環境變數 (參考 `config.py` 中的設定，如資料庫連線字串、API Key)。
3.  運行 Flask 應用程式：`flask run` 或 `python app.py`。
4.  (可能需要初始化資料庫或運行爬蟲腳本來獲取初始資料)。


