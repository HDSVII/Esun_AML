import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from bert_serving.client import BertClient
from sklearn.manifold import TSNE
from sklearn.svm import SVC

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}, {iteration}/{total}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def __consineSim(v1, v2):
    return np.divide(np.inner(v1, v2), np.multiply(np.linalg.norm(v1), np.linalg.norm(v2)))

def getSim(content1, content2):

    bc = BertClient()
    v1 = bc.encode([content1])[0]
    v2 = bc.encode([content2])[0]

    return __consineSim(v1, v2)

def parseNews(path):

    df = pd.read_csv(path)

    enc = []

    bc = BertClient()
    print('Created Bert')
    printProgressBar(0, len(df), prefix = 'News parsing progress:', suffix = 'Complete', length = 50)
    for index, news in df.iterrows():

        # enc.append(1 if len(news['name']) == 2 else 0)
        enc.append(bc.encode([news['content']])[0])
        printProgressBar(index + 1, len(df), prefix = 'News parsing progress:', suffix = 'Complete', length = 50)
        pass
    printProgressBar(len(df), len(df), prefix = 'News parsing progress:', suffix = 'Complete', length = 50)

    print('Finished parseNews')
    print('Fitting')
    return enc


# USE THIS FUNCTION
def createCls():
    train_data_dir = '/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/data/ESUN_news_3_label.csv'
    # os.path.abspath(train_data_dir)
    train_data = pd.read_csv(train_data_dir)
    # print (train_data['label_lm'])

    myCls = SVC()
    myCls.fit(parseNews(train_data_dir), train_data['label_lm']) # need to be dumped on disk~
    print('myCls fit complete.')

    return myCls

# returns true or false
# USE THIS FUNCTION
def isLaunderingWithBert(myCls, news_string) -> bool:
    """
    Usage:
    myCls = createCls() # in the beginning of api_v1.py
    result = isLaunderingWithBert(myCls, news_string) # news_string is the string of the news article
    """
    bc = BertClient()
    enc = [bc.encode(news_string)[0]]

    #svm_result = myCls.predict(parseNews('test_data.csv'))
    svm_result = myCls.predict(enc)
    
    return (svm_result[0] == 1)

    

def test_run():
    myCls = createCls()
    train_data_dir = 'train_data.csv'
    test_data_dir = 'test_data.csv'

    svm_result = myCls.predict(parseNews(test_data_dir))
    train_data = pd.read_csv(train_data_dir)
    test_data = pd.read_csv(test_data_dir)

    tpos = 0
    fpos = 0
    tneg = 0
    fneg = 0


    for pred_label, true_label in zip(svm_result, test_data['label_lm']):
        if pred_label == 1 and true_label == 1:
            tpos += 1
        elif pred_label == 1 and true_label == 0:
            fpos += 1
        elif pred_label == 0 and true_label == 0:
            tneg += 1
        elif pred_label == 0 and true_label == 1:
            fneg += 1
    print ('====test data====')
    print ('true_pos :', tpos)
    print ('false_pos:', fpos)
    print ('true_neg :', tneg)
    print ('false_neg:', fneg)
    print ('accuracy:', (tpos+tneg)/len(test_data.index))

    svm_result_train = myCls.predict(parseNews(train_data_dir))

    for pred_label, true_label in zip(svm_result_train, train_data['label_lm']):
        if pred_label == 1 and true_label == 1:
                tpos += 1
        elif pred_label == 1 and true_label == 0:
                fpos += 1
        elif pred_label == 0 and true_label == 0:
                tneg += 1
        elif pred_label == 0 and true_label == 1:
                fneg += 1

    print ('====total data====')
    print ('true_pos :', tpos)
    print ('false_pos:', fpos)
    print ('true_neg :', tneg)
    print ('false_neg:', fneg)
    print ('accuracy:', (tpos+tneg)/(len(test_data.index)+len(train_data.index)))

    # np.save('if_laundering', np.array(parseNews('ESUN_news_2.csv')))

    # X = np.load('embedding.npy')
    # Y = np.load('if_laundering.npy')

    # X_embedded = TSNE(n_components=2).fit_transform(X)

    # np.save('pca_embedding', X_embedded)

    '''
    X_embedded = np.load('pca_embedding.npy')

    for x, y in zip(X_embedded, Y):
        plt.scatter(x[0], x[1], color=('red' if y == 0 else 'blue'), s=2)

    plt.savefig('results_svm.png')
    plt.close()
    '''


if __name__ == '__main__':

    test_run()
