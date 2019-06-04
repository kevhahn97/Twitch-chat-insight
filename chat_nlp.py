import json
import re

from konlpy.tag import Okt
from collections import Counter


def main():

    filename = input("Input: ")
    with open(filename+'.json', 'r', encoding='utf-8-sig') as data_file:
        data = json.load(data_file)

    nouns_file = filename+"_nouns.txt"

    nouns = []
    nlpy = Okt()

    for contents in data:
        nouns = nouns + nlpy.nouns(contents["contents"])

    count = Counter(nouns)
    

    

    tags_count = []
    tags = []

    for n, c in count.most_common(50):
        dics = {'tag': n, 'count': c}
        tags_count.append(dics)
        tags.append(dics['tag'])

    output_file = open(nouns_file, 'w', 1, "utf-8")

    for tag in tags_count:
        print(' {:<14}\t{}\n'.format(tag['tag'], tag['count']))
        output_file.write(' {:<14}\t{}\n'.format(tag['tag'], tag['count']))

    output_file.close()
    
if __name__ == "__main__":
    main()