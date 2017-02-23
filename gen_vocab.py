import os
import json
class_names = []
paths = []
path = '/Users/Nattapat/Learnning/ML-course/naive_bayes/corenlptut/corpus/comp.windows.x'
class_names.append(path.split('/')[-1:][0])
paths.append(path)
path = '/Users/Nattapat/Learnning/ML-course/naive_bayes/corenlptut/corpus/sci.electronics'
paths.append(path)
class_names.append(path.split('/')[-1:][0])
# print(class_names)

count = 0
target_paths = {}
for path in paths:
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            # is type is json
            if(name[-4:] == "json"):
                target = os.path.join(root, name)
                count += 1
                c_name = path.split('/')[-1:][0]

                if c_name in target_paths.keys():
                    target_paths[c_name].append(target)
                else:
                    target_paths[c_name] = []
                # print(target)

print('total file = ' + str(count))
print('========================')

# print(target_paths)

VOCAB_DICT = {}
total_vocab = {}

#  inital tocal vocab in each class.
for class_name in class_names:
    total_vocab[class_name] = 0


for class_name in class_names:
    for target_path in target_paths[class_name]:

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

                            # initialize
                            for _class_name in class_names:
                                VOCAB_DICT[word][ _class_name + str("_count") ] = 0

                            currn_key = class_name + str("_count")
                            VOCAB_DICT[word][ currn_key] = 1
                            


                            # VOCAB_DICT[word][ class_name + str("_count") ] = 1

                           
                            # else:
                                # VOCAB_DICT[word][ class_name + str("_count") ] = 1

                        total_vocab[class_name] += 1

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

for class_name in class_names:
    print(class_name)
    # input()
    for word in VOCAB_DICT:
        key = class_name + str("_prob")
        # VOCAB_DICT[word][key] = VOCAB_DICT[word][ class_name + str("_count") ]
        # print(VOCAB_DICT[word][class_name +"_count"])
        VOCAB_DICT[word][key] = VOCAB_DICT[word][class_name+"_count"] / total_vocab[class_name]
    # print(word, VOCAB_DICT[word])


print(VOCAB_DICT)
# print(total_vocab)
# print(x)