import sys
import os
import re
import numpy as np
import copy

model_probs = {}
output_lines = []


def model_reader():
    modeler_path = "nbmodel.txt"
    model_params = open(modeler_path, 'r')
    for line in model_params:
        if re.search('\t', line):
            field = line.strip().split('\t')

            key = field[0]
            model_probs[key] = np.array([float(field[1]), float(field[2]), float(field[3]), float(field[4])])
    model_params.close()


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
    tokens = [i for i in tokens if len(i) > 2]
    return tokens


def cleaner(tokens):
    for i in range(len(tokens)):
        if len(tokens[i]) > 1 and tokens[i][-1] == 's':
            try:
                model_probs[tokens[i][0:-1]]
                tokens[i] = tokens[i][0:-1]
            except KeyError:
                pass

        if len(tokens[i]) > 2 and (tokens[i][-2:] == 've' or 'nt' or 'ly' or 'ed'):
            try:
                model_probs[tokens[i][0:-2]]
                tokens[i] = tokens[i][0:-2]
            except KeyError:
                pass

    return tokens


def naive_bayes(path):
    for (root, dirs, files) in os.walk(path):
        for file in files:
            if len(file) > 4 and str(file)[-4:] == '.txt':

                value = 0.0
                class_probs = copy.deepcopy(model_probs['prior_probs'])

                with open(str(root) + "/" + str(file), 'r') as f:
                    tokens = tokenizer(f)
                    tokens = cleaner(tokens)
                    f.close()

                for token in tokens:
                    try:
                        for i in [0, 1, 2, 3]:
                            value = copy.deepcopy(class_probs[i] * model_probs[token][i])
                            class_probs[i] = value

                    except KeyError:
                        pass

                if np.sum([class_probs[0], class_probs[2]]) > np.sum([class_probs[1], class_probs[3]]):
                    label_a = 'truthful'

                else:
                    label_a = 'deceptive'

                if class_probs[0] + class_probs[1] > class_probs[2] + class_probs[3]:
                    label_b = 'positive'

                else:
                    label_b = 'negative'

                output_lines.append(str(label_a) + " " + str(label_b) + " " + str(root) + "/" + str(file) + "\n")

    with open("nboutput.txt", "w+") as output:
        for lines in output_lines:
            output.write(str(lines))
        output.close()


def classifier():
    path = sys.argv[1]
    model_reader()
    naive_bayes(path)


if __name__ == "__main__":
    classifier()
