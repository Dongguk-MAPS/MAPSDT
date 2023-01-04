from tqdm import tqdm
from colorama import Style, Fore
from time import sleep
import numpy as np
import time
from collections import deque
from sympy import simplify
from sympy import sympify


class Data(object):
    def __init__(self, keys, values):
        for (key, value) in zip(keys, values):
            self.__dict__[key] = value
        self.id = 0
        self.winner = ''
        self.usedCategorical = []
        self.predict = None


class Attribute:
    def __init__(self):
        self.name = None
        self.type = None
        self.new = False
        self.use = False
        self.unit = None


class Leaf:
    def __init__(self):
        self.rule = ''
        self.dataset = []
        self.terminateBuilding = False
        self.branch = 0
        self.parent = None
        self.id = None
        self.branchAttribute = None
        self.classes = None
        self.decision = []
        self.predict = None


class Chromosome:
    def __init__(self, attribute, data):
        self.string = []
        self.expression = ''
        self.attribute = attribute
        self.data = data

    def combine(self):
        s = deque()
        operation = ['+', '*', '-', '/', 'attr', 'BLANK']
        operation2 = ['+', '*', '-', '/']
        operation3 = ['attr']
        operation4 = ['BLANK']
        possible = None
        for e in self.string:
            if e not in operation:
                s.append(e)
            elif e in operation3:
                n1 = s.pop()
                s.append('obj.' + n1.name)
            elif e == operation4:
                pass
            elif e in operation2:
                n1 = s.pop()
                n2 = s.pop()

                if (type(n1) == Attribute) and (type(n2) == Attribute):
                    s.append('(obj.' + n2.name + e + 'obj.' + n1.name + ')')
                elif (type(n1) != Attribute) and (type(n2) == Attribute):
                    s.append('(' + n2.name + e + 'obj.' + n1 + ')')
                elif (type(n1) == Attribute) and (type(n2) != Attribute):
                    s.append('(obj.' + n2 + e + n1.name + ')')
                else:
                    s.append('(' + n2 + e + n1 + ')')

                if check_proper_calc(n1, e, n2, self.attribute):
                    possible = True
                else:
                    possible = False
                    return False
        if possible:
            try:
                list(map(lambda obj: eval(s[0]), self.data))
                self.expression = s[0]
                return True
            except:
                return False


class Population:
    def __init__(self):
        self.population = []


class DT:
    def __init__(self):
        self.leaf = list
        self.root = None
        self.test_data = None
        self.rule_decision = list
        self.accuracy = 0
        self.chromosome = None

    def fit(self):
        self.root.dataset = self.test_data
        decisions = sorted(list(set(map(lambda x: x.Decision, self.test_data))))
        num_of_decisions = []
        for i in decisions:
            num_of_decisions.append(list(map(lambda x: x.Decision, self.root.dataset)).count(i))
        self.root.decision = num_of_decisions
        # for _leaf in tqdm(self.leaf, desc=Fore.GREEN + Style.BRIGHT + "Fitting : ", mininterval=0.1, ncols=150):
        for _leaf in self.leaf:
            _leaf.dataset = []
            # for i in list(filter(lambda obj:eval(_leaf.rule), _leaf.parent.dataset)):
            #
            #     i.predict = _leaf.predict
            #     _leaf.dataset.append(i)

            for obj in _leaf.parent.dataset:
                if eval(_leaf.rule):
                    obj.predict = _leaf.predict
                    _leaf.dataset.append(obj)

            num_of_decisions = []
            for i in decisions:
                num_of_decisions.append(list(map(lambda x: x.Decision, _leaf.dataset)).count(i))
            _leaf.decision = num_of_decisions
            sleep(0.1)


def attribute_set(attribute, data):
    # attribute 의 데이터 타입(범주형 or 연속형)을 판단
    if len(set(map(lambda x: x.__getattribute__(attribute.name), data))) <= 8:
        attribute.type = 'Categorical'
        for _data in data:
            setattr(_data, attribute.name, str(_data.__getattribute__(attribute.name)))
    else:
        attribute.type = 'Continuous'


def get_wine_unit(attr_name):
    if attr_name == "fixedacidity":
        return "g/dm^3"
    elif attr_name == "volatileacidity":
        return "g/dm^3"
    elif attr_name == "citricacid":
        return "g/dm^3"
    elif attr_name == "residualsugar":
        return "g/dm^3"
    elif attr_name == "chlorides":
        return "g/dm^3"
    elif attr_name == "freesulfurdioxide":
        return "mg/dm^3"
    elif attr_name == "totalsulfurdioxide":
        return "mg/dm^3"
    elif attr_name == "density":
        return "g/cm^3"
    elif attr_name == "sulphates":
        return "g/dm^3"
    elif attr_name == "pH":
        return "pH"
    elif attr_name == "alcohol":
        return "percent"


def get_steel_unit(attr_name):
    if attr_name == "X_Minimum":
        return "Area"
    elif attr_name == "X_Maximum":
        return "Area"
    elif attr_name == "Y_Minimum":
        return "Area"
    elif attr_name == "Y_Maximum":
        return "Area"
    elif attr_name == "Pixels_Areas":
        return "Area"
    elif attr_name == "X_Perimeter":
        return "m"
    elif attr_name == "Y_Perimeter":
        return "m"
    elif attr_name == "Sum_of_Luminosity":
        return "W"
    elif attr_name == "Minimum_of_Luminosity":
        return "W"
    elif attr_name == "Maximum_of_Luminosity":
        return "W"
    elif attr_name == "Length_of_Conveyer":
        return "m"
    elif attr_name == "Steel_Plate_Thickness":
        return "m"
    elif attr_name == "Edges_Index":
        return "Index"
    elif attr_name == "Empty_Index":
        return "Index"
    elif attr_name == "Square_Index":
        return "Index"
    elif attr_name == "Outside_X_Index":
        return "Index"
    elif attr_name == "Edges_X_Index":
        return "Index"
    elif attr_name == "Edges_Y_Index":
        return "Index"
    elif attr_name == "Outside_Global_Index":
        return "Index"
    elif attr_name == "LogOfAreas":
        return "Area"
    elif attr_name == "Log_X_Index":
        return "Index"
    elif attr_name == "Log_Y_Index":
        return "Index"
    elif attr_name == "Orientation_Index":
        return "Index"
    elif attr_name == "Luminosity_Index":
        return "Index"
    elif attr_name == "SigmoidOfAreas":
        return "Area"


def check_proper_calc(attr1, oper, attr2, attribute):
    def check_unit(attr):
        if type(attr) == Attribute:
            return attr.unit
        elif (attr.count('obj.') == 1) or (attr.count('obj.') == 0):
            attr = attr.replace('(', '').replace(')', '').replace('obj.', '')
            try:
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
            except:
                unit = ' '
                print()
            return unit
        else:
            attr = attr.replace('(', '').replace(')', '').replace('obj.', '')
            if '+' in attr:
                attr = attr.split('+')[0]
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
                return unit
            elif '-' in attr:
                attr = attr.split('-')[0]
                unit = list(filter(lambda x: x.name == attr, attribute))[0].unit
                return unit
            elif '*' in attr:
                attr = attr.split('*')
                attr1, attr2 = attr[0], attr[1]
                unit1 = check_unit(attr1)
                unit2 = check_unit(attr2)
                unit = str(sympify(unit1 + '*' + unit2))
                return unit
            elif '/' in attr:
                attr = attr.split('/')
                attr1, attr2 = attr[0], attr[1]
                unit1 = check_unit(attr1)
                unit2 = check_unit(attr2)
                unit = str(sympify(unit1 + '/' + unit2))
                return unit

    if oper == "+" or oper == "-":  # Unit Conversion Not Needed - Just Check Valid Operation
        if check_unit(attr1) != check_unit(attr2):
            return False  # Invalid Operation
        else:
            return True  # Valid Operation

    else:  # Unit Conversion Needed (* or /)
        # new_unit = simplify("(" + check_unit(attr1) + ")" + oper + "(" + check_unit(attr2) + ")")
        return True
