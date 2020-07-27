from flask import Flask
from flask import request
from flask import jsonify
import datetime
import pickle
import hashlib
import sys
import numpy as np
import pandas as pd

# sys.path.append('./bert_classification')
# sys.path.append('./NER-BERT-pytorch')

from bert_classification.client_SVM import createCls, isLaunderingWithBert
from NER_BERT_pytorch.evaluate import evaluate_config
from NER_BERT_pytorch.NerToResult import extractName


app = Flask(__name__)
####### PUT YOUR INFORMATION HERE #######
CAPTAIN_EMAIL = 'kaoweitse220@gmail.com'          #
SALT = 'ai-samurai'                        #
#########################################

# data_loader, model, params = evaluate_config()
# print('name extraction configured')
# myCls = createCls() # fit
# print('myCls created')


# Initiate prediction models
# Load necessary data from pickle files
print('Loading preprocessed data.')
data_loader, model, params, myCls = None, None, None, None
with open('data_loader.pickle', 'rb') as pickle_file:
    data_loader = pickle.load(pickle_file)

with open('model.pickle', 'rb') as pickle_file:
    model = pickle.load(pickle_file)

with open('params.pickle', 'rb') as pickle_file:
    params = pickle.load(pickle_file)

with open('myCls.pickle', 'rb') as pickle_file:
    myCls = pickle.load(pickle_file)

print('Preprocessed data loaded.')



def generate_server_uuid(input_string):
    """ Create your own server_uuid
    @param input_string (str): information to be encoded as server_uuid
    @returns server_uuid (str): your unique server_uuid
    """
    s = hashlib.sha256()
    data = (input_string+SALT).encode("utf-8")
    s.update(data)
    server_uuid = s.hexdigest()
    return server_uuid

def predict(article):
    """ Predict your model result
    @param article (str): a news article
    @returns prediction (list): a list of name
    """

    ####### PUT YOUR MODEL INFERENCING CODE HERE #######
    prediction = []
    article = bytes(article, 'utf-8').decode('utf-8','ignore')


    is_laundering = isLaunderingWithBert(myCls, article)
    print('is_laundering result:{}'.format(is_laundering))
    if is_laundering:
        # perform name extraction here
        print('performing prediction')
        prediction = extractName(data_loader, model, params, article)
        print('prediction result:{}'.format(prediction))

    # defult anser: ['aha','danny','jack']
    
    
    ####################################################
    prediction = _check_datatype_to_list(prediction)
    return prediction

def _check_datatype_to_list(prediction):
    """ Check if your prediction is in list type or not. 
        And then convert your prediction to list type or raise error.
        
    @param prediction (list / numpy array / pandas DataFrame): your prediction
    @returns prediction (list): your prediction in list type
    """
    if isinstance(prediction, np.ndarray):
        _check_datatype_to_list(prediction.tolist())
    elif isinstance(prediction, pd.core.frame.DataFrame):
        _check_datatype_to_list(prediction.values)
    elif isinstance(prediction, list):
        return prediction
    raise ValueError('Prediction is not in list type.')

@app.route('/healthcheck', methods=['POST'])
def healthcheck():
    """ API for health check """
    data = request.get_json(force=True)  

    # log writing
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write('API call: healthcheck\n')
        log_file.write('{}\n'.format(str(data)))

    t = datetime.datetime.now()  
    ts = str(int(t.utcnow().timestamp()))
    server_uuid = generate_server_uuid(CAPTAIN_EMAIL+ts)
    server_timestamp = t.strftime("%Y-%m-%d %H:%M:%S")

    return_data = {'esun_uuid': data['esun_uuid'], 'server_uuid': server_uuid, 'captain_email': CAPTAIN_EMAIL, 'server_timestamp': server_timestamp}

    # log writing
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write('Response\n')
        log_file.write('{}\n'.format(str(return_data)))

    return jsonify(return_data)



@app.route('/inference', methods=['POST'])
def inference():
    """ API that return your model predictions when E.SUN calls this API """
    data = request.get_json(force=True)  
    esun_timestamp = data['esun_timestamp'] #自行取用
    
    t = datetime.datetime.now()  
    ts = str(int(t.utcnow().timestamp()))
    server_uuid = generate_server_uuid(CAPTAIN_EMAIL+ts)


    # log writing
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write('API call: inference\n')
        log_file.write('{}\n'.format(str(data)))

    # write articles
    with open('articles.txt', 'a', encoding='utf-8') as articles_file:
        articles_file.write('{}\n'.format(data['news']))
    
    try:
        answer = predict(data['news'])
    except:
        raise ValueError('Model error.')        
    server_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return_data = {'esun_timestamp': data['esun_timestamp'], 'server_uuid': server_uuid, 'answer': answer, 'server_timestamp': server_timestamp, 'esun_uuid': data['esun_uuid']}

    # log writing
    with open('log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write('Response\n')
        log_file.write('{}\n'.format(str(return_data)))

    return jsonify(return_data)




if __name__ == "__main__":
    # Test prediction functionality
    sentence = ''
    with open('NER_BERT_pytorch/ner_test.txt', 'r', encoding='utf-8') as test:
        sentence = test.read()
    sentence = bytes(sentence, 'utf-8').decode('utf-8','ignore')

    print('Prediction check:')
    print(predict(sentence))

    print('Name extraction check:')
    print(extractName(data_loader, model, params, sentence))

    print('Waiting for api call...')

    app.run(host='0.0.0.0', port=8081, debug=True)
