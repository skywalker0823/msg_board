# Steps of develop
為解決上傳圖片時會卡住的問題，應將上傳圖片的部分改為非同步處理。
1. For asynchronus needs, pip installed celery and redis
2. Run redis with docker : docker run -dp 6379:6379 redis:5(you can use redis-cli to check if it is running locally and successfully)
3. 將app.py 設置好後在另一個terminal執行 celery -A app.celery worker --loglevel=info
4. 啟動 flask