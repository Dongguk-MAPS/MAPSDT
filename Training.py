import math
import copy
from time import sleep
from tqdm import tqdm
from colorama import Style, Fore
import data_load as data_load
from Genetic_Programming import GPFE
from functions import calculateEntropy, processContinuousFeatures
from sympy import sympify


def buildDecisionTree(config):
    train_data, attribute, test_data = config['train_data'], config['attribute'], config['test_data']
    attribute_new = copy.deepcopy(attribute)
    max_depth = config['max_depth']
    geneticProgramming = config['Genetic Programming']
    if geneticProgramming:
        cntnAttr = list(filter(lambda x: x.type is 'Continuous', attribute_new))
        forest = GPFE(cntnAttr, attribute_new, config)
        best_tree = sorted(forest, key=lambda x: x.accuracy, reverse=True)[0]
        return best_tree.rule_decision, best_tree.leaf, best_tree.root

    winner_attribute, train_data = findGains(train_data, attribute_new, 1, max_depth, config)
    if winner_attribute.type is 'Continuous':
        classes = list(set(map(lambda x: x.winner, train_data)))

    else:
        classes = list(set(map(lambda x: x.__getattribute__(winner_attribute.name), train_data)))

    # =========================================
    root = data_load.Leaf()
    root.id = '1'
    root.branchAttribute = winner_attribute.name
    leaf_list = []  # 모든 leaf
    result_leaf = []  # terminateBuilding 이 True 인 leaf

    decisions = [str(i) for i in range(len(config['target_names']))]

    # =========================================

    # for _leaf, _index in enumerate(tqdm(range(len(classes)), desc=Fore.GREEN + Style.BRIGHT + "Creating Root...           ", mininterval=0.1,ncols=150)):
    for _leaf, _index in enumerate(range(len(classes))):
        _leaf = data_load.Leaf()
        if winner_attribute.type is 'Continuous':
            if 'obj.' in winner_attribute.name:
                _leaf.rule += str(winner_attribute.name) + ' ' + str(classes[_index])
            else:
                _leaf.rule += 'obj.' + str(winner_attribute.name) + ' ' + str(classes[_index])
            processed_data = list(filter(lambda x: x.winner == classes[_index], train_data))

        else:
            _leaf.rule += 'obj.' + str(winner_attribute.name) + ' == ' + "'" + str(classes[_index]) + "'"
            processed_data = list(
                filter(lambda x: x.__getattribute__(winner_attribute.name) == classes[_index], train_data))

        _leaf.parent = root
        _leaf.id = '1' + str(_index)
        _leaf.classes = classes[_index]

        # =========================================

        _leaf.dataset = processed_data
        num_of_decisions = []
        for i in decisions:
            num_of_decisions.append(list(map(lambda x: x.Decision, _leaf.dataset)).count(i))
        _leaf.decision = num_of_decisions
        for i in _leaf.dataset:
            train_data.remove(i)
        # =========================================

        if winner_attribute.type is 'Categorical':
            for i in _leaf.dataset:
                i.usedCategorical.append(winner_attribute.name)
                delattr(i, winner_attribute.name)

        # =========================================

        if len(set(map(lambda x: x.Decision, _leaf.dataset))) == 1:
            _leaf.terminateBuilding = True
            result_leaf.append(_leaf)

        # =========================================
        _leaf.branch += 1
        _leaf.predict = decisions[num_of_decisions.index(max(num_of_decisions))]
        leaf_list.append(_leaf)
        sleep(0.1)

    # =========================================
    depth = 2
    while len(set(filter(lambda x: x.terminateBuilding is False, leaf_list))) >= 1:
        notTerminated = list(filter(lambda x: x.terminateBuilding is False, leaf_list))
        # for _leaf in tqdm(notTerminated, desc=Fore.GREEN + Style.BRIGHT + "Creating Tree...(Depth = " + str(depth) + ')', mininterval=0.1, ncols=150):
        for _leaf in notTerminated:

            attribute_new = copy.deepcopy(attribute)
            if geneticProgramming:
                cntnAttr = list(filter(lambda x: x.type is 'Continuous', attribute_new))
                chromosome_list = GPFE(cntnAttr, attribute_new, _leaf.dataset, test_data, config)
                for _chrom in chromosome_list:
                    new_attribute = data_load.Attribute()
                    new_attribute.name = _chrom.chromosome
                    new_attribute.type = 'Continuous'
                    new_attribute.new = True
                    attribute_new.append(new_attribute)
                    for obj in _leaf.dataset:
                        setattr(obj, new_attribute.name, eval(new_attribute.name))
            winner_attribute, _leaf.dataset = findGains(_leaf.dataset, attribute_new, depth, max_depth, config)
            _leaf.branchAttribute = winner_attribute.name
            if winner_attribute.type is 'Continuous':
                classes = list(set(map(lambda x: x.winner, _leaf.dataset)))

            else:
                classes = list(set(map(lambda x: x.__getattribute__(winner_attribute.name), _leaf.dataset)))

            # =========================================

            for _child_leaf, _index in enumerate(range(len(classes))):
                _child_leaf = data_load.Leaf()
                _child_leaf.branch = _leaf.branch + 1
                _child_leaf.rule = _leaf.rule + ' and '
                _child_leaf.classes = classes[_index]
                if winner_attribute.name != 'Decision':
                    if winner_attribute.type is 'Continuous':
                        if 'obj.' in winner_attribute.name:
                            _child_leaf.rule += str(winner_attribute.name) + str(classes[_index])
                        else:
                            _child_leaf.rule += 'obj.' + str(winner_attribute.name) + str(classes[_index])
                        processed_data = list(filter(lambda x: x.winner == classes[_index], _leaf.dataset))
                    else:
                        _child_leaf.rule += 'obj.' + str(winner_attribute.name) + ' == ' + "'" + str(
                            classes[_index]) + "'"
                        processed_data = list(
                            filter(lambda x: x.__getattribute__(winner_attribute.name) == classes[_index],
                                   _leaf.dataset))

                    _child_leaf.parent = _leaf
                    _child_leaf.id = _child_leaf.parent.id + str(_index)

                    # =========================================

                    _child_leaf.dataset = processed_data
                    num_of_decisions = []
                    for i in decisions:
                        num_of_decisions.append(list(map(lambda x: x.Decision, _child_leaf.dataset)).count(i))
                    _child_leaf.decision = num_of_decisions
                    for i in _child_leaf.dataset:
                        _leaf.dataset.remove(i)

                    # =========================================

                    if winner_attribute.type is 'Categorical':
                        for i in _child_leaf.dataset:
                            i.usedCategorical.append(winner_attribute.name)
                            delattr(i, winner_attribute.name)

                    # =========================================

                    if not _child_leaf.terminateBuilding:
                        if len(set(map(lambda x: x.Decision, _child_leaf.dataset))) == 1:
                            _child_leaf.terminateBuilding = True
                            result_leaf.append(_child_leaf)

                        if _child_leaf.branch >= max_depth:
                            _child_leaf.terminateBuilding = True
                            result_leaf.append(_child_leaf)

                    # =========================================
                    _child_leaf.predict = decisions[num_of_decisions.index(max(num_of_decisions))]
                    leaf_list.append(_child_leaf)
            _leaf.terminateBuilding = True
            result = [i for i in result_leaf]
            rule_decision = []
            for i in result:
                rule_decision.append([i.rule, max(list(map(lambda x: x.Decision, i.dataset)),
                                                  key=list(map(lambda x: x.Decision, i.dataset)).count)])
            sleep(0.1)
            # =========================================
        depth += 1
    return rule_decision, leaf_list, root


def findGains(data, attribute, depth, max_depth, config):
    GR_correction = config['GR_correction']
    gains = []
    entropy = calculateEntropy(data)
    attribute = list(filter(lambda x: x.name not in data[0].usedCategorical, attribute))
    for _index in range(len(attribute)):
        if attribute[_index].name != 'Decision':
            if attribute[_index].type is 'Continuous':
                data = processContinuousFeatures(data, attribute[_index], entropy, depth, max_depth, config)
                classes = set(map(lambda x: x.winner, data))
            else:
                classes = set(map(lambda x: x.__getattribute__(attribute[_index].name), data))

            # =========================================

            splitinfo = 0
            gain = entropy

            for j in range(0, len(classes)):
                current_class = list(classes)[j]
                if attribute[_index].type is 'Continuous':
                    subdataset = list(filter(lambda x: x.winner == current_class, data))
                else:
                    subdataset = list(
                        filter(lambda x: x.__getattribute__(attribute[_index].name) == current_class, data))

                subset_instances = len(subdataset)
                class_probability = subset_instances / len(data)

                subset_entropy = calculateEntropy(subdataset)
                gain = gain - class_probability * subset_entropy

                if not GR_correction:
                    splitinfo = splitinfo - class_probability * math.log(class_probability, 2)
                elif GR_correction:
                    splitinfo = splitinfo + (math.log(subset_instances) - (
                            class_probability * math.log(subset_instances * class_probability, 2)))

            if splitinfo == 0:
                splitinfo = 100  # this can be if data set consists of 2 rows and current column consists of 1 class. still decision can be made (decisions for these 2 rows same). set splitinfo to very large value to make gain ratio very small. in this way, we won't find this column as the most dominant one.

            if not GR_correction:
                gain = gain / splitinfo
            elif GR_correction:
                gain = gain / (1 + splitinfo)
            gains.append(gain)
    winner_index = gains.index(max(gains))

    if (attribute[winner_index].name == '0') or (attribute[winner_index].name == '1') or (
            attribute[winner_index].name == '2') or (attribute[winner_index].name == '1/2'):
        winner_index += 1

    if attribute[winner_index].name == 'Decision':
        winner_index += 1

    winner_attribute = attribute[winner_index]
    if winner_attribute.type is 'Continuous':
        data = processContinuousFeatures(data, winner_attribute, entropy, depth, max_depth, config)
    return winner_attribute, data
