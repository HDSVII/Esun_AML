import csv
import collections
import jieba
import pandas as pd

data = pd.read_csv('ESUN_news.csv') 
# print (data)
df = pd.DataFrame(data, columns= ['content'])

for index, row in data.iterrows():
    # print (index)
    if row['name'] == '[]':
        print (index)
        print (row['content'])

# print (data['content'][1455])

# print (type(df))
# print (type(data))

# for row in df:
#     print (row)

#     for row in rows:
#         if row["name"] is not "[]":
#             seg_list = jieba.cut(row['content'])
#             # print ("\n各单词出现的次数：\n %s" % collections.Counter(seg_list))
#             cnt_content = collections.Counter(seg_list)
#             cnt_keyword.update(cnt_content)
# # 開啟 CSV 檔案
# with open('ESUN_news.csv', newline='',  encoding='utf-8') as csvfile:

#     # 讀取 CSV 檔案內容
#     rows = csv.DictReader(csvfile)
#     cnt_keyword = collections.Counter()
#     # 以迴圈輸出每一列
#     # rows = csv.reader(csvfile, delimiter=',')

#     for row in rows:
#         if row["name"] is not "[]":
#             seg_list = jieba.cut(row['content'])
#             # print ("\n各单词出现的次数：\n %s" % collections.Counter(seg_list))
#             cnt_content = collections.Counter(seg_list)
#             cnt_keyword.update(cnt_content)
#         # print(row['news_ID'], row['content'])
  
#   print(cnt_keyword)