import copy
import numpy as np
import data_load as data_load


def preprocessingData(config):
    def data_split(data, _portion: float):
        if _portion == 0:
            train_data = copy.deepcopy(data)
            test_data = copy.deepcopy(data)
        else:
            target_unique = set(map(lambda x: x[-1], data))
            target_unique_list = list([_data for _data in data if _data[-1] == _target] for _target in target_unique)
            train_data, test_data = [], []
            for _target in target_unique_list:
                train_data.extend(np.random.permutation(_target)[:int(len(_target) * (1 - _portion))])
                test_data.extend(np.random.permutation(_target)[:int(len(_target) * _portion)])

        return np.array(train_data), np.array(test_data)

    def preprocessing(config):
        df, target_names, _portion = config['data'].to_numpy(), config['target_names'], config['split_portion']
        for _index, _target_name in enumerate(target_names):
            # for i in df:
            #     if str(i[-1]) == _target_name:
            #         i[-1] = str(_index)
            df = np.where(df == _target_name, str(_index), df)

        train_data_value, test_data_value = data_split(df, _portion)
        train_data = [data_load.Data(attribute_name, train_data_value[i])
                      for i in range(train_data_value.shape[0])]
        test_data = [data_load.Data(attribute_name, test_data_value[i])
                     for i in range(test_data_value.shape[0])]
        for i in range(len(train_data)):
            train_data[i].id = i

        for i in range(len(test_data)):
            test_data[i].id = i

        attribute = []
        for _name in attribute_name:
            _name = data_load.Attribute()
            attribute.append(_name)
        for _index in range(len(attribute)):
            attribute[_index].name = attribute_name[_index]
            attribute[_index].unit = data_load.get_steel_unit(attribute[_index].name)
            data_load.attribute_set(attribute[_index], train_data)
            data_load.attribute_set(attribute[_index], test_data)

        return train_data, test_data, attribute


    attribute_name = [i.replace(' ', '') for i in config['data']]
    train_data, test_data, attribute = preprocessing(config)

    return train_data, test_data, attribute
