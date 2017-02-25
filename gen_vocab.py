import os
import json
class_names = []
paths = []

ROOT_PATH = './json'

for sub_path in os.listdir(ROOT_PATH):
    target_path = os.path.join(ROOT_PATH, sub_path)
    paths.append(target_path)
    class_names.append(sub_path)

TOTAL_FILE = 0
TARGET_PATHS = {}
for path in paths:
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # is type is json
            if name[-4:] == "json":
                target = os.path.join(root, name)
                TOTAL_FILE += 1
                c_name = path.split('/')[-1:][0]

                if c_name in TARGET_PATHS.keys():
                    TARGET_PATHS[c_name].append(target)
                else:
                    TARGET_PATHS[c_name] = []

print('total file = ' + str(TOTAL_FILE))
print('========================')


VOCAB_DICT = {}
total_vocab = {}

#  inital tocal vocab in each class.
for class_name in class_names:
    total_vocab[class_name] = 0


for class_name in class_names:
    for target_path in TARGET_PATHS[class_name]:

        try:
            f = open(target_path)
            # print(target_path)
            reader = json.load(f)
            for sentence in reader['sentences']:
                for token in sentence['tokens']:
                    word = token['originalText']
                    if word in VOCAB_DICT.keys():
                        VOCAB_DICT[word][class_name + "_count"] += 1
                    else:
                        VOCAB_DICT[word] = {}
                        for _class_name in class_names:
                            VOCAB_DICT[word][_class_name + str("_count")] = 0

                        currn_key = class_name + str("_count")
                        VOCAB_DICT[word][currn_key] = 1

                    total_vocab[class_name] += 1

        except Exception as inst:
            pass
            # print('\n====\n')
            # print('error' + str(inst))
            print(target_path)
            input()
            # print('\n====\n')

        # print(TARGET_PATHS[1])

    # print(VOCAB_DICT)
    # print(total_vocab)
    # print(x)

for class_name in class_names:
    print(class_name)
    # input()
    for word in VOCAB_DICT:
        key = class_name + str("_prob")
        # VOCAB_DICT[word][key] = VOCAB_DICT[word][ class_name + str("_count") ]
        # print(VOCAB_DICT[word][class_name +"_count"])
        VOCAB_DICT[word][key] = VOCAB_DICT[word][
            class_name + "_count"] / total_vocab[class_name]
    # print(word, VOCAB_DICT[word])


print(VOCAB_DICT)
# print(total_vocab)
# print(x)
