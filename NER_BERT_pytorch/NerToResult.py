"""Evaluate the model"""

from .evaluate import evaluate_config, evaluate

def parseName(sentence, entity_sentence):

    # sentences = [x.split() for x in originalSentences.split('\n')]
    # results = [x.split() for x in predictResults.split('\n')]

    ret = []

    # for sentence in sentences:

    current_string = ''

    for charater, entity in zip(sentence, entity_sentence):
        if entity == 'B-PER':
            if current_string != '':
                ret.append(current_string)
            current_string = charater

        elif entity == 'I-PER':
            current_string += charater

    if current_string != '':
        ret.append(current_string)

    return ret


def extractName(data_loader, model, params, original_sentence):
    # Write to sentences.txt and tags.txt to evaluate can read it
    with open('/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/temp/test/sentences.txt', 'w', encoding='utf-8') as fp:
        fp.write(' '.join(list(original_sentence)) + '\n')
    with open('/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/temp/test/tags.txt', 'w', encoding='utf-8') as tags:
        tags.write(' '.join(['O' for _ in range(len(original_sentence))]) + '\n')


    # Load sentece
    with open('/home/deepracer/DeepRacer/AI_Samurai/Esun_AML/NER_BERT_pytorch/temp/test/sentences.txt', 'r', encoding='utf-8') as fp:
        originalSentences = fp.read()
        fp.close()
    original_sentence = [x.split() for x in originalSentences.split('\n')][0]

    # Load data
    test_data = data_loader.load_data('test')

    params.test_size = test_data['size']
    params.eval_steps = params.test_size // params.batch_size
    # params.eval_steps = params.test_size
    test_data_iterator = data_loader.data_iterator(test_data, shuffle=False)
    
    entity_sentence = evaluate(model, test_data_iterator, params, mark='Test', verbose=True)


    

    return parseName(original_sentence, entity_sentence)



if __name__ == '__main__':
    # with open('temp/test/sentences.txt', 'r') as fp:
    #     originalSentences = fp.read()
    #     fp.close()

    # with open('tags.txt', 'r') as fp:
    #     predictResults = fp.read()
    #     fp.close()

    # ans = parseName(originalSentences, predictResults)

    # with open('answer.txt', 'w') as fp:
    #     fp.write(str(ans))
    #     fp.close()

    # USAGE
    # MOVE THIS TO api_v1.py
    data_loader, model, params = evaluate_config()

    # start_time = time.time()

    sentence = ''
    with open('ner_test.txt', 'r', encoding='utf-8') as test:
        sentence = test.read()
    
    
    print(extractName(data_loader, model, params, sentence))

    # print("Evaluation time: {}".format(time.time() - start_time))