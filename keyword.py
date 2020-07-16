import csv
import collections
import jieba
import pandas as pd

data = pd.read_csv('ESUN_news.csv') 
cnt_keyword = collections.Counter()
cnt_non_keyword = collections.Counter()

news_num = len(data.index)
moneynews_num = 0
nonnews_num = 0

for index, row in data.iterrows():
    if row['name'] != '[]':
        seg_list = jieba.cut(row['content'])
        seg_list = list(dict.fromkeys(seg_list))
        cnt_content = collections.Counter(seg_list)
        cnt_keyword.update(cnt_content)
        moneynews_num += 1
    else:
        seg_list = jieba.cut(row['content'])
        seg_list = list(dict.fromkeys(seg_list))
        cnt_content = collections.Counter(seg_list)
        cnt_non_keyword.update(cnt_content)
        nonnews_num += 1

print ('news_num:', news_num)
print ('moneynews_num:', moneynews_num)
print ('nonnews_num:', nonnews_num)

keyword = pd.DataFrame({'money_news':cnt_keyword, 'none_news':cnt_non_keyword})
keyword = keyword.fillna(0)
keyword['cond_prob'] = keyword['money_news']/(keyword['money_news'] + keyword['none_news'])

keyword = keyword.sort_values(by = 'cond_prob', ascending = False)
keyword.to_csv('keyword.csv')