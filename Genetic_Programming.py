import numpy as np
from data_load import Chromosome
import data_load as data_load
import copy
import Training
import MAPSC45 as mc
from data_load import DT
import pickle
from sympy import sympify
import gc


def GPFE(continuousAttr, attribute, config):
    train_data, test_data = config['train_data'], config['test_data']

    def init_population(_init_size, _continuousAttr, _attribute, _data):
        used_chromosome, population_list = [], []
        while True:
            _chromosome_list, operation, operation2 = [], ['+', '-', '*', '/'], ['+', '-', '*', '/', 'attr']
            chromosome_in_population = 10
            while len(_chromosome_list) != chromosome_in_population:
                _chr = data_load.Chromosome(_attribute, _data)

                selectOP1 = np.random.choice(operation, 1, replace=True)
                selectOP2 = np.random.choice(operation2, 2, replace=True)
                if selectOP2[0] == '-':
                    selectATTR1 = np.random.choice(_continuousAttr, 2, replace=False)
                else:
                    selectATTR1 = np.random.choice(_continuousAttr, 2, replace=True)
                if selectOP2[1] == '-':
                    selectATTR2 = np.random.choice(_continuousAttr, 2, replace=False)
                else:
                    selectATTR2 = np.random.choice(_continuousAttr, 2, replace=True)
                selectATTR = np.concatenate((selectATTR1, selectATTR2), axis=None)
                _chr.string.extend(selectOP1[0])
                _chr.string.insert(0, selectOP2[0])
                _chr.string.insert(0, selectATTR[0])
                if selectOP2[0] != 'attr':
                    _chr.string.insert(0, selectATTR[1])
                else:
                    _chr.string.insert(0, 'BLANK')
                _chr.string.insert(0, selectOP2[1])
                _chr.string.insert(0, selectATTR[2])
                if selectOP2[1] != 'attr':
                    _chr.string.insert(0, selectATTR[3])
                else:
                    _chr.string.insert(0, 'BLANK')
                if _chr.combine() == False:
                    continue
                else:
                    # _chr.combine()
                    _chromosome_list.append(_chr)
                    try:
                        list(filter(lambda obj: eval(_chr.expression) != 0, train_data))
                    except:
                        _chromosome_list.remove(_chr)

            new_attribute_list = copy.deepcopy(_attribute)
            data = copy.deepcopy(_data)
            for _chromosome in _chromosome_list:
                new_attribute = data_load.Attribute()
                new_attribute.name = _chromosome.expression
                new_attribute.type = 'Continuous'
                new_attribute.new = True
                new_attribute_list.append(new_attribute)
                for obj in data:
                    setattr(obj, new_attribute.name, eval(new_attribute.name))
            config_new = copy.deepcopy(config)
            config_new['train_data'] = data
            config_new['attribute'] = new_attribute_list
            config_new['Genetic Programming'] = False
            config_new['save'] = False

            # ==========================================

            rule_decision, leaf_list, root = Training.buildDecisionTree(config_new)
            for constructed_feature in _chromosome_list:
                if constructed_feature.expression in list(map(lambda x: x.branchAttribute, leaf_list)):
                    used_chromosome.append(constructed_feature)
            if len(used_chromosome) >= _init_size * chromosome_in_population:
                used_chromosome = used_chromosome[:_init_size * chromosome_in_population]
                break
        for i in range(_init_size):
            population = data_load.Population()
            population.population = used_chromosome[i * chromosome_in_population:(i + 1) * chromosome_in_population]
            population_list.append(population)
        forest = []
        return population_list, forest

    def fitness(_population_list, forest, _data, _attribute, test_data, config):
        for _population in _population_list:
            new_attribute_list = copy.deepcopy(_attribute)
            data = copy.deepcopy(_data)
            for _chromosome in _population.population:
                new_attribute = data_load.Attribute()
                new_attribute.name = _chromosome.expression
                new_attribute.type = 'Continuous'
                new_attribute.new = True
                new_attribute.name = str(sympify(new_attribute.name.replace('.', ''))).replace('obj', 'obj.')
                new_attribute_list.append(new_attribute)

                for obj in data:
                    try:
                        setattr(obj, new_attribute.name, eval(new_attribute.name))
                    except:
                        print()

            config_new = copy.deepcopy(config)
            config_new['train_data'] = data
            config_new['attribute'] = new_attribute_list
            config_new['Genetic Programming'] = False
            config_new['save'] = False

            # ==========================================

            rule_decision, leaf_list, root = Training.buildDecisionTree(config_new)
            tree = DT()
            tree.leaf = leaf_list
            tree.root = root
            tree.rule_decision = rule_decision
            tree.test_data = test_data
            tree.fit()
            accuracy, precision, recall, f1_score = mc.evaluate(tree.test_data)
            tree.fitness_value = accuracy
            tree.population = _population
            forest.append(tree)
            del data
            del new_attribute_list
        return forest

    def crossover_mutate(_population_list, _max_generation, forest, _data, test_data, _continuousAttr, config):
        generation, operation = 2, ['+', '-', '*', '/']
        chromosome_in_population = 10

        def tournament_selection(_forest):
            parents = np.random.choice(_forest, int(len(_forest) * 0.25), replace=False)
            parents = sorted(parents, key=lambda x: x.fitness_value, reverse=True)
            return parents[0]

        while generation <= _max_generation:
            parent = sorted(forest, key=lambda x: x.fitness_value, reverse=True)[:int(config['init_size'] * 0.1) + 1]
            parent.extend([tournament_selection(forest) for i in range(int(config['init_size'] * 0.9))])
            new_parent = []
            np.random.shuffle(parent)
            for i in range(int(len(parent) / 2)):
                child1 = copy.deepcopy(parent[i * 2])
                child2 = copy.deepcopy(parent[i * 2 + 1])
                child1.population = parent[i * 2].population.population[:int(chromosome_in_population / 2)] + parent[
                                                                                                                  i * 2 + 1].population.population[
                                                                                                              int(
                                                                                                                  chromosome_in_population / 2):]
                child2.population = parent[i * 2 + 1].population.population[:int(chromosome_in_population / 2)] + \
                                    parent[i * 2].population.population[int(chromosome_in_population / 2):]

                new_parent.append(child1)
                new_parent.append(child2)

            for _population in new_parent:
                for i in range(int(len(_population.population) / 2)):
                    _copy1 = copy.deepcopy(_population.population[i * 2])
                    _copy2 = copy.deepcopy(_population.population[i * 2 + 1])
                    # _population.population[i*2].string = _copy1.string[:3] + _copy2.string[3:]
                    mutate_probability = np.random.rand(1)[0]
                    if mutate_probability > 0.7:
                        def mutate1():
                            _operation = ['+', '-', '*', '/', 'attr']

                            selectOP = str(np.random.choice(_operation, 1, replace=True)[0])
                            if selectOP == '-':
                                selectATTR = np.random.choice(_continuousAttr, 2, replace=False)
                            else:
                                selectATTR = np.random.choice(_continuousAttr, 2, replace=True)

                            if selectOP != 'attr':
                                _population.population[i * 2].string[0] = selectATTR[0]
                                _population.population[i * 2].string[1] = selectATTR[1]
                                _population.population[i * 2].string[2] = selectOP

                            else:
                                _population.population[i * 2].string[0] = 'BLANK'
                                _population.population[i * 2].string[1] = selectATTR[1]
                                _population.population[i * 2].string[2] = selectOP

                            combine_possible = _population.population[i * 2].combine()
                            if combine_possible:
                                try:
                                    list(map(lambda obj: eval(_population.population[i * 2].expression), _data))
                                except:
                                    _population.population[i * 2] = _copy1
                                    _population.population[i * 2].combine()
                            else:
                                _population.population[i * 2] = _copy1
                                _population.population[i * 2].combine()

                        mutate1()
                    else:
                        _population.population[i * 2].string = _copy1.string[:3] + _copy2.string[3:]
                        combine_possible = _population.population[i * 2].combine()
                        if combine_possible:
                            try:
                                list(map(lambda obj: eval(_population.population[i * 2].expression), _data))
                            except:
                                _population.population[i * 2] = _copy1
                                _population.population[i * 2].combine()
                        else:
                            _population.population[i * 2] = _copy1
                            _population.population[i * 2].combine()

                    # _population.population[i*2+1].string = _copy2.string[:3] + _copy1.string[3:]
                    mutate_probability = np.random.rand(1)[0]
                    if mutate_probability > 0.7:
                        def mutate2():
                            _operation = ['+', '-', '*', '/', 'attr']

                            selectOP = str(np.random.choice(_operation, 1, replace=True)[0])
                            if selectOP == '-':
                                selectATTR = np.random.choice(_continuousAttr, 2, replace=False)
                            else:
                                selectATTR = np.random.choice(_continuousAttr, 2, replace=True)

                            if selectOP != 'attr':
                                _population.population[i * 2 + 1].string[0] = selectATTR[0]
                                _population.population[i * 2 + 1].string[1] = selectATTR[1]
                                _population.population[i * 2 + 1].string[2] = selectOP

                            else:
                                _population.population[i * 2 + 1].string[0] = 'BLANK'
                                _population.population[i * 2 + 1].string[1] = selectATTR[1]
                                _population.population[i * 2 + 1].string[2] = selectOP

                            combine_possible = _population.population[i * 2 + 1].combine()
                            if combine_possible:
                                try:
                                    list(map(lambda obj: eval(_population.population[i * 2 + 1].expression), _data))
                                except:
                                    _population.population[i * 2 + 1] = _copy2
                                    _population.population[i * 2 + 1].combine()
                            else:
                                _population.population[i * 2 + 1] = _copy2
                                _population.population[i * 2 + 1].combine()

                        mutate2()
                    else:
                        _population.population[i * 2 + 1].string = _copy2.string[:3] + _copy1.string[3:]
                        combine_possible = _population.population[i * 2 + 1].combine()
                        if combine_possible:
                            try:
                                list(map(lambda obj: eval(_population.population[i * 2 + 1].expression), _data))
                            except:
                                _population.population[i * 2 + 1] = _copy2
                                _population.population[i * 2 + 1].combine()
                        else:
                            _population.population[i * 2 + 1] = _copy2
                            _population.population[i * 2 + 1].combine()

                    del _copy1
                    del _copy2
                    gc.collect()

            new_forest = []
            forest = fitness(new_parent, new_forest, _data, attribute, test_data, config)
            print(generation, ' Generation completed...')
            if config['best_tree'].fitness_value <= sorted(forest, key=lambda x: x.fitness_value, reverse=True)[
                0].fitness_value:
                config['best_tree'] = sorted(forest, key=lambda x: x.fitness_value, reverse=True)[0]

            print(config['best_tree'].fitness_value * 100)
            if config['save']:
                with open('tree/' + 'Depth' + str(config['max_depth']) + '_' + str(generation) + 'generation' + '.p',
                          'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
                    pickle.dump(config['best_tree'], file)
                f = open(
                    'test-output/' + 'Depth' + str(config['max_depth']) + '_' + str(generation) + 'generation' + '.txt',
                    'w')
                for i in config['best_tree'].rule_decision:
                    rule = i[0] + '=' + str(config['target_names'][int(i[1])] + '\n')
                    f.write(rule)
            generation += 1
            del parent
            gc.collect()

        return forest

    init_size = config['init_size']
    population_list, forest = init_population(init_size, continuousAttr, attribute, train_data)
    forest = fitness(population_list, forest, train_data, attribute, test_data, config)
    print('\nInitial population completed...')
    config['best_tree'] = sorted(forest, key=lambda x: x.fitness_value, reverse=True)[0]
    print(config['best_tree'].fitness_value * 100)
    if config['save']:
        with open('tree/' + 'Depth' + str(config['max_depth']) + '_' + str(1) + 'generation' + '.p', 'wb') as file:
            pickle.dump(config['best_tree'], file)
        f = open('test-output/' + 'Depth' + str(config['max_depth']) + '_' + str(1) + 'generation' + '.txt', 'w')
        for i in config['best_tree'].rule_decision:
            rule = i[0] + '=' + str(config['target_names'][int(i[1])] + '\n')
            f.write(rule)
    max_generation = config['max_generations']
    forest = crossover_mutate(population_list, max_generation, forest, train_data, test_data, continuousAttr, config)
    return forest
