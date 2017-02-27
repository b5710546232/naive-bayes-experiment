'''
@author nattapat sukpootanan 5710546232
'''
import os
import json
import math
import operator


'''
genreate vocaburary from directory that contain dataset
 return
in this format

example
========
dict : vacab

vocab : {
    word :{
         class_name_count : Integer
         class_name_prob : Integer
         }
    }
========

'''
def learn_naive_bayes_text(root):

    class_names = []
    paths = []
    vocab_dict = {}
    num_of_vocab_dict = {}

    # root_path = './json'
    root_path = root

    for sub_path in os.listdir(root_path):
        target_path = os.path.join(root_path, sub_path)
        paths.append(target_path)
        class_names.append(sub_path)

    total_file = 0
    target_paths = {}
    for path in paths:
        for filename in os.listdir(path):
            if filename[-4:] == "json":
                total_file += 1
                target = os.path.join(path, filename)
                c_name = path.split('/')[-1:][0]

                if c_name in target_paths.keys():
                    target_paths[c_name].append(target)
                else:
                    target_paths[c_name] = []

    # print('==========for-debug===========')
    # print('total file = ' + str(total_file))

    # print('========================')


    #  inital tocal vocab in each class.
    for class_name in class_names:
        num_of_vocab_dict[class_name] = 0

    # count add vocab
    for class_name in class_names:
        for target_path in target_paths[class_name]:

            try:
                # test must delete
                # if("./json/comp.windows.x/66422.txt.json" == target_path):
                #     print("safe :) ")
                #     input()
                # print(target_path)
                f = open(target_path)
                reader = json.load(f)
                for sentence in reader['sentences']:
                    for token in sentence['tokens']:
                        word = token['originalText']
                        word = str.lower(word)

                        # print(target_path)
                        # if("./json/sci.electronics/52434.txt.json" in target_path):
                            # print("safe :) ",word)
                            # input()
                        if word in vocab_dict.keys():
                            vocab_dict[word][class_name + "_count"] += 1
                        else:
                            vocab_dict[word] = {}
                            # give 1 to all of each class
                            for _class_name in class_names:
                                vocab_dict[word][_class_name + str("_count")] = 1

                            currn_key = class_name + str("_count")
                            vocab_dict[word][currn_key] = 1

                        num_of_vocab_dict[class_name] += 1

            except Exception as inst:
                pass
                # for debug
                # print('\n====\n')
                # print('error' + str(inst))
                # print(target_path)
                # input()
                # print('\n====\n')

    # genterate probability in each class
    # # P(wk |vj) <- nk+1/n+ |Vocabulary |

    # find |vocab|  = total_vocab
    total_vocab = 0

    for class_name in class_names:
        total_vocab += num_of_vocab_dict[class_name]

    for class_name in class_names:
        # print(class_name)
        for word in vocab_dict:
            key = class_name + str("_prob")


            # |Vocabulary | = num_of_vocab_dict[class_names]
            # n + | Vocabulary |

            #  n = num_of_vocab_dict[class_name]

            #      P(Wk|Vj)       =  nk+1 / n+ |Vocabulary |
            vocab_dict[word][key] = (vocab_dict[word][class_name + "_count"] +1) \
                                    / (num_of_vocab_dict[class_name] + total_vocab)
#  debug
    # print(vocab_dict)
    return vocab_dict, num_of_vocab_dict


"""
classify the word, and return it what is in each class.
"""
def classify_naive_bayes_text(doc, data):
    vocab, num_of_vocab_dict = data
    class_names = []
    prob_class_names = {}
    total_vocab = 0

    ans_set = {}

    for key in num_of_vocab_dict.keys():
        total_vocab += num_of_vocab_dict[key]
        class_names.append(key)

    # add prob_class_names
    for class_name in class_names:
        prob_class_names[class_name] = num_of_vocab_dict[class_name] / total_vocab

        # assign prob_class_names to ans_set
        # ans_set[class_name] = prob_class_names[class_name]

        # use log
        ans_set[class_name] = math.log(prob_class_names[class_name])
        # print(ans_set[class_name])


    for w_doc in doc:
        if(w_doc in vocab.keys()):
            for class_name in class_names:
                key = class_name + str("_prob")
                # ans_set[class_name] *= vocab[w_doc][key]
                # use log
                ans_set[class_name] += math.log(vocab[w_doc][key])

    # decending order
    sorted_ans_set = sorted(ans_set.items(), key=operator.itemgetter(1), reverse=True)

    # debug
    for key in ans_set.keys():
        val = ans_set[key]
        print(key,val)

    return sorted_ans_set[0][0]

'''
read_doc return each word of doc in list.
'''
def read_doc(doc):
    doc_list = []
    for sentence in doc['sentences']:
        for token in sentence['tokens']:
            word = token['originalText']
            word = str.lower(word)
            doc_list.append(word)
    return doc_list

'''
main function
'''
def main():
    data = learn_naive_bayes_text('./train-data')
    # file_doc = open('./test-data/elec.52723.txt.json')
    # file_doc = open('./test-data/37261.txt.json')
    # doc = json.load(file_doc)
    # doc = read_doc(doc)
    # ans = classify_naive_bayes_text(doc, data)

    valid = 0
    total = 0
    test_path = './test-data'

    for file in os.listdir(test_path):
        total += 1
        target = os.path.join(test_path, file)
        if'.DS_Store' in file:
            continue
        t_doc = open(target)
        t_doc = json.load(t_doc)
        t_doc = read_doc(t_doc)
        ans = classify_naive_bayes_text(t_doc, data)
        if file[0:3] == 'com':
            if ans[0:3] == 'com':
                valid += 1
        if file[0:3] == 'ele':
            if ans[0:3] == 'sci':
                valid += 1

    print('accuracy ', (valid/total)*100, '%')


if __name__ == '__main__':
    main()