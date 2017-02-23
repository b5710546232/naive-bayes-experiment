import os
import json

path = '/Users/Nattapat/Learnning/ML-course/naive_bayes/corenlptut/corpus/sci.electronics'
class_name = path.split('/')[-1:][0]
print(class_name)

count = 0
target_paths = []
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        # is type is json
        if(name[-4:] == "json"):
            target = os.path.join(root, name)
            count += 1
            target_paths.append(target)
            # print(target)

print('total file = ' + str(count))
print('========================')


VOCAB_DICT = {}
total_vocab = 0

x = 0
for target_path in target_paths:

    try:
        f = open(target_path)
        # print(target_path)
        reader = json.load(f)

        for item_1 in list(reader.values()):
            for item_2 in item_1:
                # print(item_2['tokens'])
                for item_3 in item_2['tokens']:
                    word = item_3['originalText']
                    # print(word)
                    # print(item_3['originalText'])
                    if word in VOCAB_DICT.keys():
                        # pass
                        VOCAB_DICT[word][class_name+"_count"] += 1
                    else:
                        # pass
                        # VOCAB_DICT[word] = 1
                        VOCAB_DICT[word] = {}
                        key = class_name + str("_count")
                        VOCAB_DICT[word][key] = 1
                    total_vocab += 1

                    # print('\n==\n')
    except Exception as inst:
        pass
        # print('\n====\n')
        # print('error' + str(inst))
        # print(target_path)
        # input()
        # print('\n====\n')

    # print(target_paths[1])

# print(VOCAB_DICT)
# print(total_vocab)
# print(x)

for word in VOCAB_DICT:
    key = class_name + str("_prob")
    VOCAB_DICT[word][key] = VOCAB_DICT[word][
        class_name + str("_count")] / total_vocab
    # print(word, VOCAB_DICT[word])


print(VOCAB_DICT)
# print(total_vocab)
# print(x)