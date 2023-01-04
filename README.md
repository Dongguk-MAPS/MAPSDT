#### MAPSDT

[![Downloads](https://pepy.tech/badge/MAPSDT)](https://pepy.tech/project/MAPSDT)
[![OS](https://img.shields.io/badge/OS-windows-red)](https://windows.com)
[![Python version](https://img.shields.io/badge/python-3.7.0-brightgreen.svg)](https://www.python.org) 
 
**Team Leader** : [Chan-gyu](https://github.com/wjk1011)  **Team Member** : [Yu-ha](https://github.com/jiyuha), [Joo-young](https://github.com/Limjooyoung), [Dong-hyun](https://github.com/donghyun305), [Ji-hoon](https://github.com/wlgns959), [Gwang-hyuk](https://github.com/panghyuk), [Yun-ju](https://github.com/YUNJU11)


### **Installation**


The easiest way to install MAPSDT framework is to download it from [PyPI](https://pypi.org/project/MAPSDT).
```
pip install MAPSDT==3.0.2
```

### Usage


The target column must be in the last column of the csv file, and the column must be named '**Decision**'.
```python
import pandas as pd
from MAPSDT import *

df = pd.read_csv('dataset/wine.csv')
target_names = ['good', 'bad']
MAPSDT(df,                          		     # Dataset
       target_names,				     # type: list
       tree=None,                   	             # You can use pre-trained trees.
       split_portion=0.3,           		     # Decide the ratio of datasets.
       max_depth=5, 		    		     # The maximum depth of the tree.
       fast_learning=False,			     # if True, the number of breakpoints for each attribute is 7.
       Genetic_Progrmmaing=False,    		     # You can use Genetic Programming for Feature Extraction.
       init_size=50,		     		     # If you use GP, set initial pool size.
       max_generations=50,          		     # If you use GP, set the maximum generations.
       save=True		    		     # You can save the decision tree.
       GR_correction=True,			     # If True, use Gain Ratio corrected by Leroux et al.(2018)
       visualizing=True,		 	     # Visualize the tree
       )
```

### **Outcomes**


Built decision tree image is stored as Visualization.gv.svg in the /test-output directory.
![image](https://user-images.githubusercontent.com/70674000/141953129-3ed83e44-561f-4508-8c58-b97f9600eb45.png)

If the Visualization.gv.svg file is not created, paste text of Visualization.gv in [Graphviz Online](https://dreampuf.github.io/GraphvizOnline/).
```
// Visualization
digraph {
	10 [label="volatileacidity
[True:37 / False:139]" color=antiquewhite4 fillcolor="slategray1;0.21022727272727273:mistyrose;0.7897727272727273" fontcolor=antiquewhite4 fontname=Arial shape=box style=striped]
	1 -> 10 [label=">10.567" arrowhead=normal color=antiquewhite4 fontname=Arial]
	11 [label="totalsulfurdioxide
[True:186 / False:117]" color=antiquewhite4 fillcolor="slategray1;0.6138613861386139:mistyrose;0.38613861386138615" fontcolor=antiquewhite4 fontname=Arial shape=box style=striped]
	1 -> 11 [label="<=10.567" arrowhead=normal color=antiquewhite4 fontname=Arial]
	100 [label="totalsulfurdioxide
[True:32 / False:137]" color=antiquewhite4 fillcolor="slategray1;0.1893491124260355:mistyrose;0.8106508875739645" fontcolor=antiquewhite4 fontname=Arial shape=box style=striped]
	10 -> 100 [label="<=0.85" arrowhead=normal color=antiquewhite4 fontname=Arial]
	101 [label="sulphates
[True:5 / False:2]" color=antiquewhite4 fillcolor="slategray1;0.7142857142857143:mistyrose;0.2857142857142857" fontcolor=antiquewhite4 fontname=Arial shape=box style=striped]
	10 -> 101 [label=">0.85" arrowhead=normal color=antiquewhite4 fontname=Arial]
	110 [label="volatileacidity
[True:162 / False:114]" color=antiquewhite4 fillcolor="slategray1;0.5869565217391305:mistyrose;0.41304347826086957" fontcolor=antiquewhite4 fontname=Arial shape=box style=striped]
	11 -> 110 [label="<=104.0" arrowhead=normal color=antiquewhite4 fontname=Arial]
	111 [label="totalsulfurdioxide
```

and built decision trees are stored as characteristic names of the trees in the /tree directory.





