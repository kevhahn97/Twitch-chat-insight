import json
import re

from konlpy.tag import Twitter
from collections import Counter


def main():

    with open('ambition3.json', 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)

    chats = ''
    chat_list = []
    nouns_file = "nouns.txt"

    for contents in data:
        chats = chats + ' ' + contents["contents"]
        chat_list.append(contents["contents"])


    nlpy = Twitter()
    nouns = nlpy.nouns(chats)

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