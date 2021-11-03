import numpy as np
import math


def findGains(data, attribute, config):
    gains = []
    entropy = calculateEntropy(data)
    attribute = list(filter(lambda x: x.name not in data[0].usedCategorical, attribute))
    for _index in range(len(attribute)):
        if attribute[_index].name != 'Decision':
            if attribute[_index].type is 'Continuous':
                data = processContinuousFeatures(data, attribute[_index], entropy)
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

                splitinfo = splitinfo - class_probability * math.log(class_probability, 2)

            if splitinfo == 0:
                splitinfo = 100  # this can be if data set consists of 2 rows and current column consists of 1 class. still decision can be made (decisions for these 2 rows same). set splitinfo to very large value to make gain ratio very small. in this way, we won't find this column as the most dominant one.
            gain = gain / splitinfo

            gains.append(gain)
    winner_index = gains.index(max(gains))

    if attribute[winner_index].name == 'Decision':
        winner_index += 1

    winner_attribute = attribute[winner_index]
    if winner_attribute.type is 'Continuous':
        data = processContinuousFeatures(data, winner_attribute, entropy)
    return winner_attribute, data


def calculateEntropy(data):
    instances = len(data)
    decisions = sorted(list(set(list(map(lambda x: x.Decision, data)))))
    entropy = 0
    for i in decisions:
        num_of_decisions = list(map(lambda x: x.Decision, data)).count(i)
        class_probability = num_of_decisions / instances
        entropy = entropy - class_probability * math.log(class_probability, 2)
    return entropy


def processContinuousFeatures(data, attribute, entropy):
    if len(set(map(lambda x: x.__getattribute__(attribute.name), data))) <= 20:
        unique_values = np.array(sorted(set(map(lambda x: x.__getattribute__(attribute.name), data))))

    else:
        unique_values = []
        data_min = np.array(list(map(lambda x: x.__getattribute__(attribute.name), data))).min()
        data_max = np.array(list(map(lambda x: x.__getattribute__(attribute.name), data))).max()
        scales = list(range(7))
        for scale in scales:
            unique_values.append(data_min + ((data_max - data_min) / (len(scales) - 1) * scale))

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
        subset1 = list(filter(lambda x: x.__getattribute__(attribute.name) <= threshold, data))
        subset2 = list(filter(lambda x: x.__getattribute__(attribute.name) > threshold, data))

        subset1_rows = len(subset1)
        subset2_rows = len(subset2)
        total_instances = len(data)

        subset1_probability = subset1_rows / total_instances
        subset2_probability = subset2_rows / total_instances



        threshold_gain = entropy - subset1_probability * calculateEntropy(subset1) - subset2_probability * calculateEntropy(subset2)
        subset_gains.append(threshold_gain)


        threshold_splitinfo = math.log(len(subset1)) - subset1_probability * math.log(len(subset1) * subset1_probability, 2) + math.log(len(subset2)) - subset2_probability * math.log(len(subset2) * subset2_probability, 2)
        gainratio = threshold_gain / (1 + threshold_splitinfo)

        subset_gainratios.append(gainratio)
    winner_one = 0
    if len(subset_gainratios) == 0:
        print(1)
    winner_one = subset_gainratios.index(max(subset_gainratios))

    winner_threshold = unique_values[winner_one]
    for i in data:
        if i.__getattribute__(attribute.name) <= winner_threshold:
            i.winner = "<=" + str(round(winner_threshold, 3))
        else:
            i.winner = ">" + str(round(winner_threshold, 3))

    return data