import time
import pickle
import numpy as np
import Training as Training
from data_load import DT


def createTree(config):
    train_data, attribute, test_data = config['train_data'], config['attribute'], config['test_data']
    start_time = time.time()
    rule_decision, leaf_list, root = Training.buildDecisionTree(config)
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

    while True:
        check = len(tree.leaf)
        prune_leaf = list(filter(lambda x: x.branchAttribute is None, tree.leaf))
        for lf in prune_leaf:
            sibling = list(filter(lambda x: x.parent == lf.parent, tree.leaf))
            if (len(set(list(map(lambda x: x.predict, sibling)))) == 1) and all(
                    sb.branchAttribute is None for sb in sibling):
                lf.parent.branchAttribute = None
                for i in sibling:
                    tree.leaf.remove(i)
        if check == len(tree.leaf):
            break

    if save:
        with open('tree/' + 'Depth' + str(max_depth) + '.p', 'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
            pickle.dump(tree, file)
        f = open('test-output/' + 'Depth' + str(config['max_depth']) + '.txt', 'w')
        for i in tree.rule_decision:
            rule = i[0] + '=' + str(config['target_names'][int(i[1])] + '\n')
            f.write(rule)

        with open('test-output/' + 'rule.py', 'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
            pickle.dump(tree, file)
        f = open('test-output/' + 'rule.py', 'w')
        for i in tree.rule_decision:
            rule = 'if ' + i[0] + ': obj.predict=' + i[1] + '\n'
            f.write(rule)

    return tree


def evaluate(test_data):
    decision = [i.Decision for i in test_data]
    prediction = [i.predict for i in test_data]
    cm = np.zeros((len(set(decision)), len(set(decision))))
    for i in test_data:
        cm[int(i.Decision), int(i.predict)] += 1

    if len(set(decision)) == 2:
        TP = cm[0][0]
        TN = cm[1][1]
        FP = cm[1][0]
        FN = cm[0][1]
        accuracy = (TP + TN) / (TP + TN + FP + FN)
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        f1_score = 2 * recall * precision / (recall + precision)
    else:
        accuracy = sum(np.diag(cm)) / np.sum(cm)
        precision = np.mean(np.diag(cm) / np.sum(cm, axis=0))
        recall = np.mean(np.diag(cm) / np.sum(cm, axis=1))
        f1_score = 2 * recall * precision / (recall + precision)
    return accuracy, precision, recall, f1_score

