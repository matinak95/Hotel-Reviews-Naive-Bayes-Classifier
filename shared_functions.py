import re




def tokenizer(review):
    extra1 = ['\n', '\t', '-', '_', '  ', '~', '&', '%', '$', '#', '@', ':', '/']
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
    # tokens = [i for i in tokens if len(i) > 2]
    return tokens




def cleaner():
    removal = set()
    for token in attributes:
        if np.sum(attributes[token]) < 10 or np.sum(attributes[token]) > 0.1 * file_counter:
            removal.add(token)
        if len(token) > 1 and token[-1] == 's':
            try:
                attributes[token[0:-1]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass

        if len(token) > 2 and (token[-2:-1] == 've' or 'nt' or 'ly'):
            try:
                attributes[token[0:-2]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass
        if len(token) > 2 and (token[-2:-1] == 'ed'):
            try:
                attributes[token[0:-1]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass

            try:
                attributes[token[0:-2]] += attributes[token]
                removal.add(token)
            except KeyError:
                pass


        if len(token) < 4:
            removal.add(token)


    for item in removal:
        attributes.pop(item)

