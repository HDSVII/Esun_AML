

def parseName(originalSentences, predictResults):

    sentences = [x.split() for x in originalSentences.split('\n')]
    results = [x.split() for x in predictResults.split('\n')]

    ret = []

    for sentence, entity_sentence in zip(sentences, results):

        current_string = ''

        for charater, entity in zip(sentence, entity_sentence):

            if entity == 'B-PER':
                if current_string != '':
                    ret.append(current_string)
                current_string = charater

            elif entity == 'I-PER':
                current_string += charater

    return ret

with open('sentences.txt', 'r') as fp:
    originalSentences = fp.read()
    fp.close()

with open('tags.txt', 'r') as fp:
    predictResults = fp.read()
    fp.close()

ans = parseName(originalSentences, predictResults)

with open('answer.txt', 'w') as fp:
    fp.write(str(ans))
    fp.close()
