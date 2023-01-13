import os
import pickle
import time
from viztree import viztree
from preProcessing import preprocessingData
import MAPSC45 as mc


def MAPSDT(df, target_names: list, tree=None, split_portion=0.3, max_depth=5, fast_learning=True, GR_correction=True,
           Genetic_Progrmmaing=False, init_size=50, max_generations=50,
           save=True,
           visualizing=True):
    config = {'data': df,
              'target_names': target_names,
              'split_portion': split_portion,
              'max_depth': max_depth,
              'fast_learning': fast_learning,
              'Genetic Programming': Genetic_Progrmmaing,
              'init_size': init_size,
              'max_generations': max_generations,
              'save': save, 'Visualizing': visualizing,
              'tree': tree,
              'GR_correction': GR_correction
              }
    total_time = time.time()
    start_time = time.time()
    df = config['data']
    split_portion = config['split_portion']
    target_names = config['target_names']
    config['train_data'], config['test_data'], config['attribute'] = preprocessingData(config)

    if not os.path.exists('tree'):
        os.makedirs('tree')
    if not os.path.exists('test-output'):
        os.makedirs('test-output')

    if config['tree'] is None:
        tree = mc.createTree(config)

    else:
        with open(config['tree'], 'rb') as file:
            tree = pickle.load(file)
            tree.leaf = list(filter(lambda x: x.branch <= config['max_depth'], tree.leaf))
            for lf in tree.leaf:
                if lf.branchAttribute != None:
                    if len(list(filter(lambda x: x.parent == lf, tree.leaf))) == 0:
                        lf.branchAttribute = None

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
        print("=================================")
        print('Creating time : ', time.time() - start_time)
    tree.test_data = config['test_data']

    # ===========================================================

    tree.fit()
    visualizing = config['Visualizing']
    if visualizing:
        viztree(tree.leaf, tree.root, config)

    accuracy, precision, recall, f1_score = mc.evaluate(tree.test_data)
    print('\nAccuracy : ', accuracy * 100, '%')
    print('Precision : ', precision * 100, '%')
    print('Recall : ', recall * 100, '%')
    print('F1 Score : ', f1_score * 100, '%')
    print('\n\nTotal time : ', time.time() - total_time)
