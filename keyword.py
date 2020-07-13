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

# print ((cnt_keyword))

#keyword = pd.DataFrame.from_dict(cnt_keyword,orient='index')
# keyword = pd.DataFrame(cnt_keyword, columns=['words', 'times'])
keyword = pd.DataFrame(cnt_keyword.items(), columns=['words', 'times'])
# non_keyword = pd.DataFrame.from_dict(cnt_non_keyword,orient='index')
# non_keyword = pd.DataFrame(cnt_non_keyword, columns=['words', 'times'])
# print (cnt_keyword)
# keyword = pd.DataFrame(cnt_keyword)

keyword = keyword.sort_values(by = 'times')
keyword.to_csv('keyword.csv')

# non_keyword = non_keyword.sort_values(by = 'times')
# non_keyword.to_csv('non_keyword.csv')