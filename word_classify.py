'''
@author nattapat sukpootanan 5710546232
'''
import os
import json


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
def gen_vocab(root):

    class_names = []
    paths = []
    vocab_dict = {}
    total_vocab = {}

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
        total_vocab[class_name] = 0

    # count add vocab
    for class_name in class_names:
        for target_path in target_paths[class_name]:

            try:
                f = open(target_path)
                # print(target_path)
                reader = json.load(f)
                for sentence in reader['sentences']:
                    for token in sentence['tokens']:
                        word = token['originalText']
                        if word in vocab_dict.keys():
                            vocab_dict[word][class_name + "_count"] += 1
                        else:
                            vocab_dict[word] = {}
                            for _class_name in class_names:
                                vocab_dict[word][_class_name + str("_count")] = 0

                            currn_key = class_name + str("_count")
                            vocab_dict[word][currn_key] = 1

                        total_vocab[class_name] += 1

            except Exception as inst:
                pass
                # for debug
                # print('\n====\n')
                # print('error' + str(inst))
                # print(target_path)
                # input()
                # print('\n====\n')

    # genterate probability in each class
    for class_name in class_names:
        # print(class_name)
        for word in vocab_dict:
            key = class_name + str("_prob")
            vocab_dict[word][key] = vocab_dict[word][
                class_name + "_count"] / total_vocab[class_name]

    return vocab_dict


def classify():
    vocab = gen_vocab('./json')

def main():
    classify()

if __name__ == '__main__':
    main()