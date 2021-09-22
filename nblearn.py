import sys
import os
import re
import numpy as np
import copy


file_counter = 0
pos_tru_num = 0
pos_dec_num = 0
neg_tru_num = 0
neg_dec_num = 0
root_path = sys.argv[1]

pos_tru_fold1 = os.path.join(root_path, "positive_polarity", "truthful_from_TripAdvisor", "fold1")
pos_tru_fold2 = os.path.join(root_path, "positive_polarity", "truthful_from_TripAdvisor", "fold2")
pos_tru_fold3 = os.path.join(root_path, "positive_polarity", "truthful_from_TripAdvisor", "fold3")
pos_tru_fold4 = os.path.join(root_path, "positive_polarity", "truthful_from_TripAdvisor", "fold4")

pos_dec_fold1 = os.path.join(root_path, "positive_polarity", "deceptive_from_MTurk", "fold1")
pos_dec_fold2 = os.path.join(root_path, "positive_polarity", "deceptive_from_MTurk", "fold2")
pos_dec_fold3 = os.path.join(root_path, "positive_polarity", "deceptive_from_MTurk", "fold3")
pos_dec_fold4 = os.path.join(root_path, "positive_polarity", "deceptive_from_MTurk", "fold4")

neg_tru_fold1 = os.path.join(root_path, "negative_polarity", "truthful_from_Web", "fold1")
neg_tru_fold2 = os.path.join(root_path, "negative_polarity", "truthful_from_Web", "fold2")
neg_tru_fold3 = os.path.join(root_path, "negative_polarity", "truthful_from_Web", "fold3")
neg_tru_fold4 = os.path.join(root_path, "negative_polarity", "truthful_from_Web", "fold4")

neg_dec_fold1 = os.path.join(root_path, "negative_polarity", "deceptive_from_MTurk", "fold1")
neg_dec_fold2 = os.path.join(root_path, "negative_polarity", "deceptive_from_MTurk", "fold2")
neg_dec_fold3 = os.path.join(root_path, "negative_polarity", "deceptive_from_MTurk", "fold3")
neg_dec_fold4 = os.path.join(root_path, "negative_polarity", "deceptive_from_MTurk", "fold4")

train_pos_tru = [pos_tru_fold2, pos_tru_fold3, pos_tru_fold4]
train_pos_dec = [pos_dec_fold2, pos_dec_fold3, pos_dec_fold4]
train_neg_tru = [neg_tru_fold2, neg_tru_fold3, neg_tru_fold4]
train_neg_dec = [neg_dec_fold2, neg_dec_fold3, neg_dec_fold4]

attributes = {}
attr_prob = {}


def file_reader():
    global file_counter
    global pos_tru_num
    global pos_dec_num
    global neg_tru_num
    global neg_dec_num
    for fold in train_pos_tru:
        for file in os.listdir(fold):
            with open(os.path.join(fold, file), 'r') as f:
                tokens = tokenizer(f)
                f.close()
                pos_tru_num += 1
                indexer(tokens, 0)
    for fold in train_pos_dec:
        for file in os.listdir(fold):
            with open(os.path.join(fold, file), 'r') as f:
                tokens = tokenizer(f)
                f.close()
                pos_dec_num += 1
                indexer(tokens, 1)
    for fold in train_neg_tru:
        for file in os.listdir(fold):
            with open(os.path.join(fold, file), 'r') as f:
                tokens = tokenizer(f)
                f.close()
                neg_tru_num += 1
                indexer(tokens, 2)
    for fold in train_neg_dec:
        for file in os.listdir(fold):
            with open(os.path.join(fold, file), 'r') as f:
                tokens = tokenizer(f)
                f.close()
                neg_dec_num += 1
                indexer(tokens, 3)

    file_counter = pos_tru_num + pos_dec_num + neg_tru_num + neg_dec_num



def tokenizer(review):
    extra1 = ['\n', '\t', '-', '_', '  ', '~', '&', '%', '$', '#', '@', ':', '/', '*']
    extra2 = ['.', ',', ';', '(', ')', '!', '?', '\"', '\'']

    text = review.read()
    text = text.lower()

    for item in extra1:
        text = text.replace(item, ' ')

    for item in extra2:
        text = text.replace(item, '')

    numbers = '[0-9]'

    tokens = text.split(' ')

    try:
        tokens = tokens.remove(' ')
    except ValueError:
        pass

    tokens = [re.sub(numbers, '', i) for i in tokens]

    return tokens


def indexer(tokens, num):
    for token in tokens:
        try:
            attributes[token][num] += 1
        except KeyError:
            attributes[token] = np.array([0, 0, 0, 0])
            attributes[token][num] += 1


def cleaner():

    stop_words = ['were', 'have', 'would', 'each', 'doing', 'travel', 'travelling', 'someone', 'guy', 'room', 'girl',
                  'daughter', 'wont', 'did', 'from', 'without', 'your', 'when', 'where', 'what', 'why', 'was',
                  'one', 'two', 'three', 'who', 'how', 'for', 'using', 'want', 'remind', 'share',
                  'seeing', 'ahead', 'indeed', 'cannot', 'bring', 'anyone',
                  'yourself', 'truly', 'heard', 'mention', 'behind', 'house', 'everywhere', 'waiting',
                  'guest', 'almost', 'throughout', 'family', 'saying', 'above', 'taking',
                  'normal', 'sitting', 'instead', 'somewhere', 'below', 'inside', 'saturday', 'bottom', 'internet',
                  'another', 'either', 'boyfriend', 'anyway', 'thought', 'themselves', 'myself',
                  'across', 'enough', 'along', 'weekend', 'morning', 'watching', 'something', 'bathroom',
                  'traveling', 'getting', 'since', 'opinion', 'taken', 'itself', 'thing', 'staying', 'first', 'again',
                  'through', 'could', 'between', 'everyone', 'everything', 'going', 'because', 'which',
                  'anywhere', 'place', 'being']
    save_short = ['bad', 'worst', 'worse', 'rat', 'not', 'shit', 'damn', 'good', 'well', 'poor', 'cheap', 'worth', 'buy', 'bath', 'dog', 'kind', 'fuck', 'hate', 'fake', 'cost', 'safe', 'warm', 'cool', 'love', 'low', 'high', 'bitch']

    removal = set()
    for i in stop_words:
        removal.add(i)

    for token in attributes:


        if np.sum(attributes[token]) < 3 or np.sum(attributes[token]) > 1 * file_counter:
            removal.add(token)
        if len(token) > 1 and token[-1] == 's':
            try:
                attributes[token[0:-1]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass

        if len(token) > 2 and (token[-2:] == 've' or 'nt' or 'ly' or 'ed'):
            try:
                attributes[token[0:-2]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass



        if len(token) < 5:
            if token not in save_short:
                removal.add(token)

    for item in removal:
        attributes.pop(item)


def smoother():
    for item in attributes:
        attributes[item] += np.array([1, 1, 1, 1])


def prob_maker():
    for key in attributes:
        attr_prob[key] = np.array([attributes[key][0]/pos_tru_num, attributes[key][1]/pos_dec_num,
                          attributes[key][2]/neg_tru_num, attributes[key][3]/neg_dec_num])

    attr_prob['prior_probs'] = np.array([pos_tru_num/file_counter, pos_dec_num/file_counter,
                                neg_tru_num/file_counter, neg_dec_num/file_counter])


def modeler():
    file = open("nbmodel.txt", "w+")
    for key in attr_prob:
        file.write(str(key) + '\t' + str(attr_prob[key][0]) + '\t' + str(attr_prob[key][1]) +
                   "\t" + str(attr_prob[key][2]) + "\t" + str(attr_prob[key][3]) + "\n")
    file.close()


def learner():
    file_reader()
    cleaner()
    smoother()
    prob_maker()
    modeler()


if __name__ == "__main__":
    learner()




