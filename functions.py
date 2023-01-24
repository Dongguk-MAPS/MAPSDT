import numpy as np
import math


def calculateEntropy(data):
    instances = len(data)
    decisions = sorted(list(set(list(map(lambda x: x.Decision, data)))))
    entropy = 0
    for i in decisions:
        num_of_decisions = list(map(lambda x: x.Decision, data)).count(i)
        class_probability = num_of_decisions / instances
        entropy = entropy - class_probability * math.log(class_probability, 2)
    return entropy


def processContinuousFeatures(data, attribute, entropy, depth, max_depth, config):
    GR_correction = config['GR_correction']
    fast_learning = config['fast_learning']
    if len(set(map(lambda x: x.__getattribute__(attribute.name), data))) <= 20:
        unique_values = np.array(sorted(set(map(lambda x: x.__getattribute__(attribute.name), data))), dtype=np.float64)

    else:
        if fast_learning:
            unique_values = []
            data_min = np.nanmin(np.array(list(map(lambda x: x.__getattribute__(attribute.name), data)), dtype=np.float64))
            data_max = np.nanmax(np.array(list(map(lambda x: x.__getattribute__(attribute.name), data)), dtype=np.float64))
            scales = list(range(7))
            for scale in scales:
                unique_values.append(data_min + ((data_max - data_min) / (len(scales) - 1) * scale))
        else:
            unique_values = []
            unique = np.unique(np.array(list(map(lambda x: x.__getattribute__(attribute.name), data)), dtype=np.float64))
            for i in range(0, len(unique)-1):
                unique_values.append((unique[i] + unique[i+1]) / 2)



    subset_gainratios = []
    subset_gains = []

    if len(unique_values) == 1:
        winner_threshold = unique_values[0]
        for i in data:
            if i.__getattribute__(attribute.name) <= winner_threshold:
                i.winner = "<=" + str(winner_threshold)
            else:
                i.winner = ">" + str(winner_threshold)
        return data

    for i in range(0, len(unique_values) - 1):
        threshold = unique_values[i]
        subset1, subset2 = [], []
        [subset1.append(i) if np.float64(i.__getattribute__(attribute.name)) <= threshold else subset2.append(i) for i in data]
        subset1_rows = len(subset1)
        subset2_rows = len(subset2)
        total_instances = len(data)

        subset1_probability = subset1_rows / total_instances
        subset2_probability = subset2_rows / total_instances

        threshold_gain = entropy - subset1_probability * calculateEntropy(
            subset1) - subset2_probability * calculateEntropy(subset2)
        subset_gains.append(threshold_gain)
        if not GR_correction:
            threshold_splitinfo = -subset1_probability * math.log(subset1_probability, 2) - subset2_probability * math.log(subset2_probability, 2)
            gainratio = threshold_gain / threshold_splitinfo

        elif GR_correction:
            threshold_splitinfo = math.log(len(subset1), 2) - subset1_probability * math.log(len(subset1) * subset1_probability, 2) + math.log(len(subset2), 2) - subset2_probability * math.log(len(subset2) * subset2_probability, 2)
            gainratio = threshold_gain / (1 + threshold_splitinfo)

        subset_gainratios.append(gainratio)
    winner_one = 0
    if len(subset_gainratios) == 0:
        print(1)
    winner_one = subset_gainratios.index(max(subset_gainratios))

    winner_threshold = unique_values[winner_one]
    for i in data:
        if i.__getattribute__(attribute.name) <= winner_threshold:
            i.winner = "<=" + str(winner_threshold)
        else:
            i.winner = ">" + str(winner_threshold)

    return data
