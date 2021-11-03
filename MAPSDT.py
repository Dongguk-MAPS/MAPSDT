import os
import pickle
import time
from viztree import viztree
from preProcessing import preprocessingData
import MAPSC45 as mc


def MAPSDT(df, tree=None, split_portion=0.3, max_depth=5, Genetic_Progrmmaing=False, init_size=50, max_generations=50,
           save=True,
           visualizing=True):
    config = {'data': df, 'split_portion': split_portion, 'max_depth': max_depth,
              'Genetic Programming': Genetic_Progrmmaing, 'init_size': init_size,
              'max_generations': max_generations, 'save': save, 'Visualizing': visualizing, 'tree': tree}
    total_time = time.time()
    start_time = time.time()
    df = config['data']
    split_portion = config['split_portion']
    train_data, test_data, attribute = preprocessingData(df, split_portion)

    if not os.path.exists('tree'):
        os.makedirs('tree')

    if config['tree'] is None:
        tree = mc.createTree(train_data, attribute, test_data, config)

    else:
        with open(config['tree'], 'rb') as file:
            tree = pickle.load(file)
        print("=================================")
        print('Creating time : ', time.time() - start_time)
    tree.test_data = test_data

    # ===========================================================

    tree.fit()
    visualizing = config['Visualizing']
    if visualizing:
        viztree(tree.leaf, tree.root)

    accuracy, precision, recall, f1_score = mc.evaluate(tree.test_data)
    print('\nAccuracy : ', accuracy * 100, '%')
    print('Precision : ', precision * 100, '%')
    print('Recall : ', recall * 100, '%')
    print('F1 Score : ', f1_score * 100, '%')
    print('\n\nTotal time : ', time.time() - total_time)
