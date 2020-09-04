import random


def write_text_from_file(filename):
    text = input('Введите текст: ')
    with open(filename, 'w') as file:
        file.write(text)


def read_text_from_file(filename):
    with open(filename) as file:
        text = file.read().replace("\n", " ")
    return text


def create_model(text):
    text = text.lower()
    symbols = '.!&'
    for symbol in symbols:
        text = text.replace(symbol, " START ")
    words = text.split()
    words_window_2 = list(map(lambda i: ' '.join(words[i:i + 2]), range(len(words) - 1)))
    model = {word: dict() for word in words_window_2}
    for i, word in enumerate(words_window_2[:-1]):
        next_word = words_window_2[i + 1].split()[1]
        model[word][next_word] = model[word].get(next_word, 0) + 1
    return model


def generate_sent(model):
    sent = ['START']
    last_word = ''
    for key in model:
        if key.split()[0] == 'START':
            last_word = key
            break
    while True:
        next_possible_words = model[last_word].keys()
        next_possible_weights = model[last_word].values()
        next_word = random.choices(list(next_possible_words), next_possible_weights)[0]
        print(next_word)
        if next_word == 'START':
            break
        sent.append(next_word)
        last_word = next_word
    sent = " ".join(sent[1:]).capitalize() + "."
    return sent


# write_text_from_file('input.txt')
text = read_text_from_file("input.txt")
model = create_model(text)
sent = generate_sent(model)
print(sent)
# print(model)
