步驟:

1. 到 https://console.cloud.google.com/ 新增專案
2. 搜尋 YouTube Data API v3 並啟用
3. 到專案下，新增 OAuth 2.0 用戶端 ID 憑證
   - 將新增的憑證 json 下載，並放在專案目錄下
   - 檔名為 client_secret_ooo.apps.googleusercontent.com.json
4. 執行程式
   1. 第一組 OAuth 帳號為 訂閱頻道 來源
   2. 第二組 OAuth 帳號為 增加訂閱頻道 目標
5. 程式結束後，第二組帳號就訂閱了第一組帳號所訂閱的頻道

範例程式碼:

https://github.com/youtube/api-samples/blob/master/python