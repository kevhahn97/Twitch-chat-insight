import codecs
import re

length_minimum = 4
set_minimum = 3
whitelist_characters = r"([^!@#$%^&*(),.?\":{}|`~<>\[\]\-_=+\\/;'a-zA-Z0-9\u3131-\u318E\uAC00-\uD7A3\u1100-\u11f9\s]|http)"


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
    if sentence[0] == "?" or sentence[1] == "?":
        return False
    return True


def is_contain_other_character(sentence, filter):
    if filter.search(sentence) is None:
        return False
    else:
        return True


filename = input("filename: ")
with open(filename, 'r', encoding='utf-8-sig') as data_file:
    data = data_file.readlines()

chat_list = list()
question_list = list()
filter_regex = re.compile(whitelist_characters)

for chatting in data:
    if chatting[-1] == "\n":
        chatting = chatting[:-1]

    # 1. check length
    if len(chatting) < length_minimum:
        continue

    # 2. check simple sentence
    if is_simple_sentence(chatting):
        continue

    # 0. filter characters
    if is_contain_other_character(chatting, filter_regex):
        continue

    chat_list.append(chatting + "\n")

    # 3. check question
    if not is_question(chatting):
        continue

    question_list.append(chatting + "\n")

with codecs.open('chat_' + filename, 'w', encoding='utf-8') as output_file:
    output_file.writelines(chat_list)
with codecs.open('question_' + filename, 'w', encoding='utf-8') as output_file:
    output_file.writelines(question_list)
