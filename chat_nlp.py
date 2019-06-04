import json
import re

from konlpy.tag import Twitter
from collections import Counter


def main():

    with open('ambition2.json', 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)

    chats = ''
    chat_list = []
    nouns_file = "nouns.txt"
    question_file = "question.txt"

    quest_output_file = open(question_file, 'w', 1, "utf-8")

    for contents in data:
        chats = chats + ' ' + contents["contents"]
        chat_list.append(contents["contents"])

    for ch in chat_list:
        m = re.search('\w+?$', ch)
        if m:
            quest_output_file.write(' {}\n'.format(m.group()))
    quest_output_file.close()

    nlpy = Twitter()
    nouns = nlpy.morphs(chats)

    count = Counter(nouns)
    tags_count = []
    tags = []

    for n, c in count.most_common(50):
        dics = {'tag': n, 'count': c}
        tags_count.append(dics)
        tags.append(dics['tag'])

    output_file = open(nouns_file, 'w', 1, "utf-8")

    for tag in tags_count:
       output_file.write(' {:<14}\t{}\n'.format(tag['tag'], tag['count']))

    output_file.close()

if __name__ == "__main__":
    main()