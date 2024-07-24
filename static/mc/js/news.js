let currentExpandedIndex = -1; // 初始值為 -1，表示沒有任何新聞被展開

// 切換新聞內容的顯示狀態
function toggleFullNews(index) {
    const fullNewsDiv = document.getElementById('full_news_' + index); // 獲取指定索引的完整新聞內容元素
    if (fullNewsDiv) {
        // 如果已有新聞展開，隱藏它
        if (currentExpandedIndex !== -1) {
            const currentFullNewsDiv = document.getElementById('full_news_' + currentExpandedIndex);
            if (currentFullNewsDiv) {
                currentFullNewsDiv.style.display = 'none'; // 隱藏當前展開的新聞
            }
        }
        // 如果點擊的是已經展開的新聞，則關閉它
        if (currentExpandedIndex === index) {
            currentExpandedIndex = -1; // 重置展開狀態
        } else {
            // 展開新聞
            fullNewsDiv.style.display = 'block'; // 顯示新選擇的新聞內容
            currentExpandedIndex = index; // 更新當前展開的新聞索引
        }
    }
}


// 顯示指定的選項卡內容
function showTab(tabId) {
    var tabContents = document.querySelectorAll('.tabcontent'); // 獲取所有選項卡內容區塊
    tabContents.forEach(function(tabContent) {
        tabContent.classList.remove('active'); // 隱藏所有選項卡內容
    });
    document.getElementById(tabId).classList.add('active'); // 顯示選擇的選項卡內容
}


// 切換新聞內容的顯示狀態（簡單的顯示/隱藏）
function toggleFullNews(id) {
    var fullNewsElement = document.getElementById('full_news_' + id); // 獲取指定 ID 的完整新聞內容元素
    if (fullNewsElement.style.display === 'none') {
        fullNewsElement.style.display = 'block'; // 顯示新聞內容
    } else {
        fullNewsElement.style.display = 'none'; // 隱藏新聞內容
    }
}
