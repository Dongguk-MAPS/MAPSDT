import time
import pickle
import numpy as np
import Training as Training
from data_load import DT


def createTree(train_data, attribute, test_data, config):
    start_time = time.time()
    rule_decision, leaf_list, root = Training.buildDecisionTree(train_data, attribute, test_data, config)
    print("\n=================================")
    print('Creating Tree : ', time.time() - start_time)
    print("=================================")

    # ===========================================================
    tree = DT()
    tree.leaf = leaf_list
    tree.root = root
    tree.rule_decision = rule_decision
    save = config['save']
    max_depth = config['max_depth']
    if save:
        with open('tree/' + 'Depth' + str(max_depth) + '.p', 'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
            pickle.dump(tree, file)

    return tree


def evaluate(test_data):
    decision = [i.Decision for i in test_data]
    prediction = [i.predict for i in test_data]
    cm = np.zeros((len(set(decision)), len(set(decision))))
    for i in test_data:
        cm[int(i.Decision), int(i.predict)] += 1

    recall = np.mean(np.diag(cm) / np.sum(cm, axis=1))
    precision = np.mean(np.diag(cm) / np.sum(cm, axis=0))
    accuracy = sum(np.diag(cm)) / np.sum(cm)
    f1_score = 2*recall*precision / (recall + precision)

    return accuracy, precision, recall, f1_score

