import csv
import collections
import jieba
import pandas as pd

data = pd.read_csv('ESUN_news.csv') 
cnt_keyword = collections.Counter()
cnt_non_keyword = collections.Counter()

for index, row in data.iterrows():
    if row['name'] != '[]':
        seg_list = jieba.cut(row['content'])
        seg_list = list(dict.fromkeys(seg_list))
        cnt_content = collections.Counter(seg_list)
        cnt_keyword.update(cnt_content)
    else:
        seg_list = jieba.cut(row['content'])
        seg_list = list(dict.fromkeys(seg_list))
        cnt_content = collections.Counter(seg_list)
        cnt_non_keyword.update(cnt_content)

keyword = pd.DataFrame(cnt_keyword.items(), columns=['words', 'times'])

test = pd.DataFrame({'money_news':cnt_keyword, 'none_news':cnt_non_keyword})

# non_keyword = pd.DataFrame(cnt_non_keyword.items(), columns=['words', 'times'])

# keyword = keyword.sort_values(by = 'times', ascending = False)
# keyword.to_csv('keyword.csv')

# non_keyword = non_keyword.sort_values(by = 'times', ascending = False)
# non_keyword.to_csv('non_keyword.csv')
test.to_csv('test.csv')