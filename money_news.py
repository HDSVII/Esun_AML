import pandas as pd 

data = pd.read_csv('ESUN_news.csv')
keywords = pd.read_csv('keyword_filted.csv', index_col=[0])

score_list = []
score_threshold = 10

news_num = len(data.index)

true_pos = 0
false_pos = 0
false_neg = 0
true_neg = 0

for index, row in data.iterrows():
    keywscore = 0
    for keyw_idx, keyw_row in keywords.iterrows():
        if keyw_idx in row['content']:
            keywscore += keyw_row['cond_prob']
    score_list.append(keywscore)
    print (index)
    if row['name'] == '[]' and keywscore < score_threshold:
        true_neg += 1
    elif row['name'] == '[]' and keywscore > score_threshold:
        false_pos += 1
    elif row['name'] != '[]' and keywscore > score_threshold:
        true_pos += 1
    elif row['name'] != '[]' and keywscore < score_threshold:
        false_neg += 1
    # if row['name'] == '[]':
    #     print (index, 'none, score', keywscore)
    # else:
    #     print (index, 'yes, score', keywscore)
data['keyw_scores'] = score_list
data.to_csv('ESUN_news_score.csv')

print ('True Positive:', true_pos)
print ('False Positive:', false_pos)
print ('False Negative:', false_neg)
print ('True Negative:', true_neg)
print ('Accuracy:', (true_pos+true_neg)/news_num)