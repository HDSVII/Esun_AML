import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bert_serving.client import BertClient
from sklearn.manifold import TSNE
from sklearn.svm import SVC

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
	for index, news in df.iterrows():

		# enc.append(1 if len(news['name']) == 2 else 0)
		enc.append(bc.encode([news['content']])[0])
		print('Bert encoding: {}'.format(index))
		pass

	return enc


# USE THIS FUNCTION
def createCls():
    train_data_dir = 'data/ESUN_news_3_label.csv'
    train_data = pd.read_csv(train_data_dir)
    # print (train_data['label_lm'])

    myCls = SVC()
    myCls.fit(parseNews(train_data_dir), train_data['label_lm'])

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