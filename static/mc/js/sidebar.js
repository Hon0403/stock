// sidebar.js

// 確保 DOM 完全加載後再執行下面的代碼
$(document).ready(function() {
    // 為每個側邊欄項目（li）註冊點擊事件處理器
    $('.sidebar > li').click(function() {
        // 當前點擊的側邊欄項目的子元素 ul 進行顯示/隱藏切換
        $(this).children('ul').slideToggle(); // 使用 slideToggle() 函數添加動畫效果
    });
});

