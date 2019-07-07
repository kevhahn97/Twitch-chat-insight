import codecs
import re
import time


# Parameter
length_minimum = 4
set_minimum = 3
whitelist_characters = r"([^!@#$%^&*(),.?\":{}|`~<>\[\]\-_=+\\/;'a-zA-Z0-9\u3131-\u318E\uAC00-\uD7A3\u1100-\u11f9\s]|http)"


# Utility function
def get_chats(filename):
    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        return data_file.readlines()


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


def is_contain_other_character(sentence, character_filter):
    if character_filter.search(sentence) is None:
        return False
    else:
        return True


def is_duplicated(sentence, sentence_set):
    if sentence in sentence_set:
        return True
    else:
        return False


def clean_chats(chats):
    start_time = time.time()

    chat_set = set()
    chat_list = list()
    question_list = list()

    filter_regex = re.compile(whitelist_characters)

    processed_chat_count = [0, 0]  # chat, question
    skipped_chat_count = [0, 0, 0, 0]  # filter, length, simple, duplicate

    for chat in chats:
        if chat[-1] == "\n":
            chat = chat[:-1]

        # 1. check length
        if len(chat) < length_minimum:
            skipped_chat_count[1] += 1
            continue

        # 2. check simple sentence
        if is_simple_sentence(chat):
            skipped_chat_count[2] += 1
            continue

        # 0. filter characters
        if is_contain_other_character(chat, filter_regex):
            skipped_chat_count[0] += 1
            continue

        # 3. check duplication
        if is_duplicated(chat, chat_set):
            skipped_chat_count[3] += 1
            continue

        chat_set.add(chat)
        chat_list.append(chat + "\n")
        processed_chat_count[0] += 1

        # 4. check question
        if not is_question(chat):
            continue

        question_list.append(chat + "\n")
        processed_chat_count[1] += 1

    print("Cleaning time: %.3f secs" % (time.time() - start_time))

    return chat_list, question_list, [processed_chat_count, skipped_chat_count]


def save_chats_and_questions(filename, chat_list, question_list):
    filename_split = filename.split(".")
    chat_filename = ".".join(filename_split[:-1]) + "_chat." + filename_split[-1]
    question_filename = ".".join(filename_split[:-1]) + "_question." + filename_split[-1]

    with codecs.open(chat_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(chat_list)
    with codecs.open(question_filename, 'w', encoding='utf-8') as output_file:
        output_file.writelines(question_list)


def analyze_result(count):
    processed = count[0]
    skipped = count[1]

    total_skipped = sum(skipped)
    total = total_skipped + processed[0]

    print("")
    print("Total chats: %d" % total)
    print("Skipped chats: %d (%.2f%%)" % (total_skipped, total_skipped / total * 100))
    print("  0. Skipped chats by char filter : %d (%.2f%%)" % (skipped[0], skipped[0] / total_skipped * 100))
    print("  1. Skipped chats by short length: %d (%.2f%%)" % (skipped[1], skipped[1] / total_skipped * 100))
    print("  2. Skipped chats by simplicity  : %d (%.2f%%)" % (skipped[2], skipped[2] / total_skipped * 100))
    print("  3. Skipped chats by duplication : %d (%.2f%%)" % (skipped[3], skipped[3] / total_skipped * 100))
    print("Processed chats: %d (%.2f%%)" % (processed[0], processed[0] / total * 100))
    print("  Processed normal chats: %d (%.2f%%)" % (processed[0] - processed[1], 100 - (processed[1] / processed[0] * 100)))
    print("  Processed questions   : %d (%.2f%%)" % (processed[1], processed[1] / processed[0] * 100))


# Main function
def main():
    filename = input("filename: ")
    chats = get_chats(filename)
    chat_list, question_list, count = clean_chats(chats)
    save_chats_and_questions(filename, chat_list, question_list)
    analyze_result(count)


if __name__ == "__main__":
    main()
