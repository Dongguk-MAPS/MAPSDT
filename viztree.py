from graphviz import Digraph
from sympy import sympify

def viztree(leaf_list, root, config):
    leaf_id = list(map(lambda x: [x.id, x.branchAttribute, x.parent, x.classes, x.decision], leaf_list))
    for _leaf in leaf_id:
        if type(_leaf[1]) == str:
            _leaf[1] = _leaf[1].replace('obj.', '')
            _leaf[1] = str(sympify(_leaf[1]))
    dot = Digraph(comment='Visualization', format='svg')
    color = ['slategray1', 'mistyrose', 'papayawhip', 'antiquewhite4', 'lightgoldenrodyellow', 'honeydew2', 'snow2', 'lightcyan1', 'lavenderblush']
    if len(leaf_id[0][4]) == 2:
        for i in leaf_id:
            if sum(i[4]) > 0:
                bar = color[0] + ';' + str(i[4][0] / sum(i[4])) + ':' + color[1] + ';' + str(i[4][1] / sum(i[4]))
            else:
                bar = color[0] + ';0.5:' + color[1] + ';0.5'
            if i[1] is None:
                if i[4][0] == i[4][1] == 0:
                    label = config['target_names'][0]+':' + str(i[4][0]) + ' / ' + config['target_names'][1]+':' + str(i[4][1]) + '\n'
                    dot.node(i[0], label, style='filled', fillcolor=color[2], fontname='Arial', fontcolor=color[3],
                             color=color[2])
                elif i[4][0] < i[4][1]:
                    decision = config['target_names'][1]
                    label = config['target_names'][0]+':' + str(i[4][0]) + ' / ' + config['target_names'][1]+':' + str(i[4][1]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='red'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                else:
                    decision = config['target_names'][0]
                    label = config['target_names'][0]+':' + str(i[4][0]) + ' / ' + config['target_names'][1]+':' + str(i[4][1]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='blue'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
            else:
                dot.node(i[0], i[1] + '\n['+config['target_names'][0]+':' + str(i[4][0]) + ' / '+config['target_names'][1]+':' + str(i[4][1]) + ']',
                        color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=bar,
                        fontcolor=color[3])
            if i[2] is '1':
                dot.edge(i[2], i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])
            else:
                dot.edge(i[2].id, i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])

        # ===========================================================

        root_bar = color[0] + ';' + str(root.decision[0] / sum(root.decision)) + ':' + color[1] + ';' + str(
            root.decision[1] / sum(root.decision))


        dot.node('1', root.branchAttribute + '\n['+config['target_names'][0]+':' + str(root.decision[0]) + ' / '+config['target_names'][1]+':' + str(
            root.decision[1]) + ']', color=color[3], shape='box', fontname='Arial', style='striped',
                fillcolor=root_bar, fontcolor=color[3])

    elif len(leaf_id[0][4]) == 3:
        for i in leaf_id:
            if sum(i[4]) > 0:
                bar = color[0] + ';' + str(i[4][0] / sum(i[4])) + ':' + color[1] + ';' + str(
                    i[4][1] / sum(i[4])) + ':' + color[4] + ';' + str(i[4][2] / sum(i[4]))
            else:
                bar = color[0] + ';1/3:' + color[1] + ';1/3' + color[4] + ';1/3'
            if i[1] is None:
                if i[4][0] == i[4][1] == i[4][2] == 0:
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + '\n'
                    dot.node(i[0], label, style='filled', fillcolor=color[2], fontname='Arial', fontcolor=color[3],
                             color=color[2])
                elif i[4][1] < i[4][0] and i[4][2] < i[4][0]:
                    decision = config['target_names'][0]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='blue'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][1] and i[4][2] < i[4][1]:
                    decision = config['target_names'][1]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='red'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                else:
                    decision = config['target_names'][2]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='gold'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
            else:

                dot.node(i[0],
                        i[1] + '\n['+config['target_names'][0]+': ' + str(i[4][0]) + ' / '+config['target_names'][1]+': ' + str(
                            i[4][1]) + ' / '+config['target_names'][2]+': ' + str(
                                 i[4][2]) + ']',
                        color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=bar,
                        fontcolor=color[3])
            if i[2] is '1':
                dot.edge(i[2], i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])
            else:
                dot.edge(i[2].id, i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])

        # ===========================================================

        root_bar = color[0] + ';' + str(root.decision[0] / sum(root.decision)) + ':' + color[1] + ';' + str(
            root.decision[1] / sum(root.decision)) + ':' + color[4] + ';' + str(root.decision[2] / sum(root.decision))


        dot.node('1',
                root.branchAttribute + '\n['+config['target_names'][0]+': ' + str(
                    root.decision[0]) + ' / '+config['target_names'][1]+': ' + str(
                    root.decision[1]) + ' / '+config['target_names'][2]+': ' + str(root.decision[2]) + ']',
                color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=root_bar,
                fontcolor=color[3])

    elif len(leaf_id[0][4]) == 4:
        for i in leaf_id:
            if sum(i[4]) > 0:
                bar = color[0] + ';' + str(i[4][0] / sum(i[4])) + ':' + color[1] + ';' + str(
                    i[4][1] / sum(i[4])) + ':' + color[4] + ';' + str(i[4][2] / sum(i[4])) + ':' + color[5] + ';' + str(i[4][3] / sum(i[4]))
            else:
                bar = color[0] + ';1/4:' + color[1] + ';1/4' + color[4] + ';1/4' + color[5] + ';1/4'
            if i[1] is None:
                if i[4][0] == i[4][1] == i[4][2] == i[4][3] == 0:
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + ' / ' + config['target_names'][3]+': ' + str(i[4][3]) + '\n'
                    dot.node(i[0], label, style='filled', fillcolor=color[2], fontname='Arial', fontcolor=color[3],
                             color=color[2])
                elif i[4][1] < i[4][0] and i[4][2] < i[4][0] and i[4][3] < i[4][0]:
                    decision = config['target_names'][0]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + ' / ' + config['target_names'][3]+': ' + str(i[4][3]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='blue'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][1] and i[4][2] < i[4][1] and i[4][3] < i[4][1]:
                    decision = config['target_names'][1]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + ' / ' + config['target_names'][3]+': ' + str(i[4][3]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='red'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][2] and i[4][1] < i[4][2] and i[4][3] < i[4][2]:
                    decision = config['target_names'][2]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + ' / ' + config['target_names'][3]+': ' + str(i[4][3]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='green'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                else:
                    decision = config['target_names'][3]
                    label = config['target_names'][0]+': ' + str(i[4][0]) + ' / ' + config['target_names'][1]+': ' + str(i[4][1]) + ' / ' + config['target_names'][2]+': ' + str(
                        i[4][2]) + ' / ' + config['target_names'][3]+': ' + str(i[4][3]) + '\n'
                    dot.node(i[0], "<" + label + "<font color='gold'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
            else:


                dot.node(i[0],
                        i[1] + '\n['+config['target_names'][0]+': ' + str(i[4][0]) + ' / ' +config['target_names'][1]+': ' + str(
                            i[4][1]) + ' / '+config['target_names'][2]+': ' + str(
                            i[4][2]) + ' / '+config['target_names'][3]+': ' + str(i[4][3]) + ']',
                        color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=bar,
                        fontcolor=color[3])
            if i[2] is '1':
                dot.edge(i[2], i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])
            else:
                dot.edge(i[2].id, i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])

        # ===========================================================

        root_bar = color[0] + ';' + str(root.decision[0] / sum(root.decision)) + ':' + color[1] + ';' + str(
            root.decision[1] / sum(root.decision)) + ':' + color[4] + ';' + str(root.decision[2] / sum(root.decision)) + ':' + color[5] + ';' + str(root.decision[3] / sum(root.decision))

        dot.node('1',
            root.branchAttribute + '\n['+config['target_names'][0]+': ' + str(
                root.decision[0]) + ' / '+config['target_names'][1]+': ' + str(
                    root.decision[1]) + ' / '+config['target_names'][2]+': ' + str(root.decision[2]) + ' / '+config['target_names'][3]+': ' + str(root.decision[3]) + ']',
                color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=root_bar,
                ontcolor=color[3])

    elif len(leaf_id[0][4]) == 7:
        for i in leaf_id:
            if sum(i[4]) > 0:
                bar = color[0] + ';' + str(i[4][0] / sum(i[4])) + ':' + \
                      color[1] + ';' + str(i[4][1] / sum(i[4])) + ':' + \
                      color[4] + ';' + str(i[4][2] / sum(i[4])) + ':' + \
                      color[5] + ';' + str(i[4][3] / sum(i[4])) + ':' + \
                      color[6] + ';' + str(i[4][4] / sum(i[4])) + ':' + \
                      color[7] + ';' + str(i[4][5] / sum(i[4])) + ':' + \
                      color[8] + ';' + str(i[4][6] / sum(i[4])) + ':'
            else:
                bar = color[0] + ';1/7' + color[1] + ';1/7' + color[4] + ';1/7' + color[5] + ';1/7' + color[6] + ';1/7' + color[7] + ';1/7' + color[8] + ';1/7'
            if i[1] is None:
                if i[4][0] == i[4][1] == i[4][2] == i[4][3] == i[4][4] == i[4][5] == i[4][6] == 0:
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], label, style='filled', fillcolor=color[2], fontname='Arial', fontcolor=color[3],
                             color=color[2])
                elif i[4][1] < i[4][0] and i[4][2] < i[4][0] and i[4][3] < i[4][0] and i[4][4] < i[4][0] and i[4][5] < i[4][0] and i[4][6] < i[4][0]:
                    decision = config['target_names'][0]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='blue'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][1] and i[4][2] < i[4][1] and i[4][3] < i[4][1] and i[4][4] < i[4][1] and i[4][5] < i[4][1] and i[4][6] < i[4][1]:
                    decision = config['target_names'][1]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='red'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][2] and i[4][1] < i[4][2] and i[4][3] < i[4][2] and i[4][4] < i[4][2] and i[4][5] < i[4][2] and i[4][6] < i[4][2]:
                    decision = config['target_names'][2]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='green'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][3] and i[4][1] < i[4][3] and i[4][2] < i[4][3] and i[4][4] < i[4][3] and i[4][5] < i[4][3] and i[4][6] < i[4][3]:
                    decision = config['target_names'][3]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='pink'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][4] and i[4][1] < i[4][4] and i[4][2] < i[4][4] and i[4][3] < i[4][4] and i[4][5] < i[4][4] and i[4][6] < i[4][4]:
                    decision = config['target_names'][4]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='black'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                elif i[4][0] < i[4][5] and i[4][1] < i[4][5] and i[4][2] < i[4][5] and i[4][3] < i[4][5] and i[4][4] < i[4][5] and i[4][6] < i[4][5]:
                    decision = config['target_names'][5]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='gray'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
                else:
                    decision = config['target_names'][6]
                    label = config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' + \
                            config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' + \
                            config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' + \
                            config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' + \
                            config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' + \
                            config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' + \
                            config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' + \
                            '\n'
                    dot.node(i[0], "<" + label + "<font color='gold'><br/>" + decision + "<br/></font>>",
                             fontcolor=color[3], color=color[3], fontname='Arial')
            else:

                dot.node(i[0],
                     i[1] + '\n['+
                     config['target_names'][0] + ': ' + str(i[4][0]) + ' / ' +
                     config['target_names'][1] + ': ' + str(i[4][1]) + ' / ' +
                     config['target_names'][2] + ': ' + str(i[4][2]) + ' / ' +
                     config['target_names'][3] + ': ' + str(i[4][3]) + ' / ' +
                     config['target_names'][4] + ': ' + str(i[4][4]) + ' / ' +
                     config['target_names'][5] + ': ' + str(i[4][5]) + ' / ' +
                     config['target_names'][6] + ': ' + str(i[4][6]) + ' / ' +
                     ']',
                     color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=bar,
                     fontcolor=color[3])
            if i[2] is '1':
                dot.edge(i[2], i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])
            else:
                dot.edge(i[2].id, i[0], i[3], fontname='Arial', arrowhead='normal', color=color[3])

        # ===========================================================

        root_bar = color[0] + ';' + str(root.decision[0] / sum(root.decision)) + ':' + \
                   color[1] + ';' + str(root.decision[1] / sum(root.decision)) + ':' + \
                   color[4] + ';' + str(root.decision[2] / sum(root.decision)) + ':' + \
                   color[5] + ';' + str(root.decision[3] / sum(root.decision)) + ':' + \
                   color[6] + ';' + str(root.decision[4] / sum(root.decision)) + ':' + \
                   color[7] + ';' + str(root.decision[5] / sum(root.decision)) + ':' + \
                   color[8] + ';' + str(root.decision[6] / sum(root.decision))


        dot.node('1',
             root.branchAttribute + '\n[' +
             config['target_names'][0] + ': ' + str(root.decision[0]) + ' / ' +
             config['target_names'][1] + ': ' + str(root.decision[1]) + ' / ' +
             config['target_names'][2] + ': ' + str(root.decision[2]) + ' / ' +
             config['target_names'][3] + ': ' + str(root.decision[3]) + ' / ' +
             config['target_names'][4] + ': ' + str(root.decision[4]) + ' / ' +
             config['target_names'][5] + ': ' + str(root.decision[5]) + ' / ' +
             config['target_names'][6] + ': ' + str(root.decision[6]) +
             ']',
             color=color[3], shape='box', fontname='Arial', style='striped', fillcolor=root_bar,
             fontcolor=color[3])
    print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
    dot.render('test-output/Visualization.gv', view=True)
