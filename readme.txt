這是2015年多媒體技術概論期末作業。

本程式碼實作兩種CBIR的方法。

使用環境

本程式須執行於ubuntu系統(14.04以後)

Python 2.7.6
Mongodb 3.0.4
opencv (包含 opencv_contrib)

Python套件：
numpy
pymongo
scipy
bottle(若需使用到網頁服務)


使用方法

1. 先將Caltech101置於與caltech2db.py同路徑

Caltech架構如下

Caltech101 --- 101_ObjectCategories  --- anchor -- image_XXXX.jpg
                                       |
                                       |
                                       |-bass -- image_XXXX.jpg

2.執行 caltech2db.py

3.執行 bow.py (目前bow.py是使用picture_list2.txt做為參考，表示使用哪些類別)

4.可選擇下面三種方法
  
  (1) 執行 cbir1.py [圖片路徑]   (如： python cbir1.py Caltech101/101_ObjectCategories/snoopy/image_0023.jpg)

  (2) 執行 cbir1.py [圖片路徑]   (如： python cbir2.py Caltech101/101_ObjectCategories/snoopy/image_0023.jpg)

  (3) 執行 index.py 將會於8080port開啟 網頁服務 (注意須提供/tmp擁有寫入權)





