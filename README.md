# MAPSDT

[![Downloads](https://pepy.tech/badge/MAPSDT)](https://pepy.tech/project/MAPSDT)
[![OS](https://img.shields.io/badge/OS-windows-red)](https://windows.com)
[![Python version](https://img.shields.io/badge/python-3.7.0-brightgreen.svg)](https://www.python.org) 
 
**Team Leader** : [Chan-gyu](https://github.com/wjk1011)  **Team Member** : [Yu-ha](https://github.com/jiyuha)


**Installation**

The easiest way to install MAPSDT framework is to download it from [PyPI](https://pypi.org/project/MAPSDT).
```
pip install MAPSDT==0.1.5
```

**Usage**
```python
import pandas as pd
from MAPSDT import *

df = pd.read_csv('dataset/wine.csv')
MAPSDT(df,
       tree=None,
       split_portion=0.3,
       max_depth=5,
       Genetic_Progrmmaing=False,
       init_size=50,
       max_generations=50,
       save=True
       )
```

**Outcomes**
Built decision tree images are stored as .svg and .gv in the /test-output directory.

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


![image](https://user-images.githubusercontent.com/70674000/141953129-3ed83e44-561f-4508-8c58-b97f9600eb45.png)


**Model save and restoration**

You can save your trained models. This makes your model ready for transfer learning.

```python
MAPSDT(save=True)
```
