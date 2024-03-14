# 建立反向索引
> 使用pyserini建立維基百科文章反向索引

## 安裝套件
請先輸入以下指令更新套件
```=
$ sudo apt-get update
$ pip install --upgrade pip
```
下載java
```=
$ sudo apt-get install openjdk-11-jdk
```
下載pyserini
```=
$ pip install pyserini
```
下載faiss
```=
$ pip install faiss-cpu --no-cache
```

## 資料預處裡
> 因後續訓練模型資料需求，將原始文章切為256、512、1024三種不同長度分別建立反向索引
  - 資料必須包含"id"和"contents" (pyserini限制)
  - 可以在資料加入其他項目，如inner_id、title等等
  - 以json格式輸出
  ```data
  [
    {"id": 1, "contents": 文章內容1},
    {"id": 2, "contents": 文章內容2},
    {"id": 3, "contents": 文章內容3}
  ]
  ```  

