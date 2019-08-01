import re
from collections import Counter, namedtuple


def parse_data(path):
    file = open(path, 'r', encoding='utf-8').read()
    pattern = re.compile(r'<content>(.*?)</content>', re.S)
    contents = pattern.findall(file)
    contents = [i for i in contents if i != '']
    return contents


def ngram(document, N=2):
    ngram_prediction = dict()
    total_grams = list()
    words = list()
    Word = namedtuple('Word', ['word', 'prob'])
    for doc in document:
        split_words = ['<s>'] + list(doc) + ['</s>']
        # 分子
        [total_grams.append(tuple(split_words[i: i+N])) for i in range(len(split_words)-N+1)]
        # 分母
        [words.append(tuple(split_words[i:i+N-1])) for i in range(len(split_words)-N+2)]
    total_word_counter = Counter(total_grams)
    word_counter = Counter(words)
    for key in total_word_counter:
        word = ''.join(key[:N - 1])
        if word not in ngram_prediction:
            ngram_prediction.update({word: set()})
        next_word_prob = total_word_counter[key] / word_counter[key[:N - 1]]
        w = Word(key[-1], '{:.3g}'.format(next_word_prob))
        ngram_prediction[word].add(w)
    return ngram_prediction


def predict(text, predictions):
    for word, ng in predictions.items():
        predictions[word] = sorted(ng, key=lambda x: x.prob, reverse=True)
    try:
        next_words = list(predictions[text])[:5]
        for next_word in next_words:
            print('下个字/符号: {} 的可能性为: {}'.format(next_word.word, next_word.prob))
    except Exception:
        raise Exception('请再输入两个字')


if __name__ == '__main__':
    data = parse_data('./Sohu.dat')
    predictions = ngram(data, N=3)
    seg = input('请输入两个字:')
    predict(seg, predictions)
