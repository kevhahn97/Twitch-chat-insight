import codecs

length_minimum = 4
set_minimum = 3


def is_simple_sentence(sentence):
    characters = set()
    for char in sentence:
        if char not in characters:
            characters.add(char)
            if len(characters) >= set_minimum:
                return False
    return True


def is_question(sentence):
    if "?" not in sentence:
        return False
    if "http" in sentence:
        return False
    if sentence[0] == "?" or sentence[1] == "?":
        return False
    return True


filename = input("filename: ")
with open(filename, 'r', encoding='utf-8-sig') as data_file:
    data = data_file.readlines()

chat_list = list()
question_list = list()

for chatting in data:
    if chatting[-1] == "\n":
        chatting = chatting[:-1]
    if len(chatting) < length_minimum:
        continue
    if is_simple_sentence(chatting):
        continue
    chat_list.append(chatting + "\n")
    if not is_question(chatting):
        continue
    question_list.append(chatting + "\n")

with codecs.open('chat_' + filename, 'w', encoding='utf-8') as output_file:
    output_file.writelines(chat_list)
with codecs.open('question_' + filename, 'w', encoding='utf-8') as output_file:
    output_file.writelines(question_list)
