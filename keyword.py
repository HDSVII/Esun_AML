import csv
import collections
import jieba
import pandas as pd

data = pd.read_csv('ESUN_news.csv') 
cnt_keyword = collections.Counter()

for index, row in data.iterrows():
    if row['name'] != '[]':
        seg_list = jieba.cut(row['content'])
        cnt_content = collections.Counter(seg_list)
        cnt_keyword.update(cnt_content)

print (cnt_keyword)