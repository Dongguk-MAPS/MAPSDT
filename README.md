# MAPSDT

[![Downloads](https://pepy.tech/badge/MAPSDT)](https://pepy.tech/project/MAPSDT)
[![OS](https://img.shields.io/badge/OS-windows-red)](https://windows.com)
[![Python version](https://img.shields.io/badge/python-3.7.0-brightgreen.svg)](https://www.python.org) 
 
## Author : [Lee Chan-gyu](https://github.com/wjk1011)

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
       save=True,		    		     # You can save the decision tree.
       GR_correction=True,			     # If True, use Gain Ratio corrected by Leroux et al.(2018)
       visualizing=True,		 	     # Visualize the tree
       )
       
"""
전체 흐름도

preprocessingData에서 데이터 스플릿, 데이터를 column마다 객체화
creatTree에서 buildDecisionTree으로 DT를 만들고, 새로운 나무에 만든 DT를 보완하여 적용 

       create와 build를 분리한 이유
       1.buildDecisionTree로 나무를 만들고, 완성된 나무를 보고 필요한 또 다른 기능이 있을까봐 분리는 해놨지만 현재는 가지치기 기능만 있음
       
       2.train으로 build하고 test에 적용한 나무는 create라고 봐도 무방


buildDecisionTree에 진입할 때, GP=True이면 GP로 buildDecisionTree를 n세대까지 반복
        GP=False이면 limited_height까지 나무 생성
        
               노드 이름 규칙 (각 노드의 부모나 자식 노드에 접근하기 쉽게하기 위해 아래 처럼 규칙에 맞게 생성)
               규칙: 부모이름+몇번째자식인지
               ex) 부모이름: 10, 3번째자식: 2
                   노드이름 = 102
                   
                               1
                         10         11
                     100   101   110  111
               
               나무 생성과정
                     층별로 균등하게 자라도록 설계되어있음
                     
                     1층
                     1. findGains로 분기할 attribute 찾기 (winner_attribute)
                     2. train 샘플 분기
       
                     1층 이후
                     왼쪽부터 오른쪽으로 생성
                     1. 분기 종료조건 검사
                     2. findGains로 분기할 attribute 찾기 (winner_attribute)
                     3. 해당 노드의 샘플 분기
                     4. 해당 층 분기가 끝나면 다음 층 가장 왼쪽노드부터 1.~3. 반복
                     
                     * 생성한 나무의 정보를 저장하고 새로운 나무에 보완하여 적용예정이라, 분기마다 노드의 정보는 다 저장
                     
                     * findGains에서 비효율적인 흐름 있음.
                            2.에서 winner_attribute를 찾으려고 계산한 결과를 저장못해놔서, 3.에서 해당 attribute를 다시 계산함
       
       
       GP=True이면,
              □:연속형변수       ○: 연산자 
              gene = □□ⓐ□□ⓑ①
              chromosome = □□○□□○○□□○□□○○□□○□□○○...□□○□□○○□□○□□○○□□○□□○○
              population = □□○□□○○□□○□□○○□□○□□○○...□□○□□○○□□○□□○○□□○□□○○
                           □□○□□○○□□○□□○○□□○□□○○...□□○□□○○□□○□□○○□□○□□○○
                           □□○□□○○□□○□□○○□□○□□○○...□□○□□○○□□○□□○○□□○□□○○
                           □□○□□○○□□○□□○○□□○□□○○...□□○□□○○□□○□□○○□□○□□○○
              
              population 만드는 과정
              1. ①에 들어갈 연산자 뽑기
              2. ⓐⓑ에 들어갈 연산자 뽑기
              
              3-1. ⓐ가 + -면 단위가 같은 연속형 변수 2개 뽑아서 ⓐ앞 □□에 배치
              3-2. ⓐ가 * /면 랜덤 연속형 변수 2개 뽑아서 ⓐ앞 □□에 배치
              3-3. ⓐ가 'ATTR'이면 랜덤 연속형 변수 1개 뽑아서 ⓐ앞에 □'BLANK'로 배치 (길이 7 항상 유지하기 위해)
              
              4-1. ⓑ가 + -면 단위가 같은 연속형 변수 2개 뽑아서 ⓑ앞 □□에 배치
              4-2. ⓑ가 * /면 랜덤 연속형 변수 2개 뽑아서 ⓑ앞 □□에 배치
              4-3. ⓑ가 'ATTR'이면 랜덤 연속형 변수 1개 뽑아서 ⓑ앞에 □'BLANK'로 배치 (길이 7 항상 유지하기 위해)
              
              5. □□ⓐ와 □□ⓑ의 연산 결과 ①로 연산 가능한지 검사
                     불가능하다면 해당 gene 삭제 후 다시 생성
                     가능하다면 저장
              
              crossover 예시 (함수명으로 없음 line: 158~169)
                     
                     population = 1234567 1234567 1234567 ... 1234567
                                  abcdefg abcdefg abcdefg ... abcdefg
                     ->
                     population = 1234567 1234567 abcdefg ... abcdefg
                                  abcdefg abcdefg 1234567 ... 1234567
                     
                     세대마다 population내 chromosome의 순서는 shuffle됨
                     
              mutate1() = 짝수번째 gene 돌연변이 
                     돌연변이 확률 30%
                     발생했다면:
                            1234567 -> ㄱㄴㄷ4567
                            연산 불가능하다면 1234567로 회귀
                     발생안했다면 옆 gene(abcdefg)와 교환:       
                            1234567 abcdefg
                            -> abc4567 123defg
                            연산 불가능한 gene이 있다면 다시 원상복귀
                            
              mutate2() = 홀수번째 gene 돌연변이 
                     돌연변이 확률 30%
                     발생했다면:
                            1234567 -> ㄱㄴㄷ4567
                            연산 불가능하다면 1234567로 회귀
                     발생안했다면 옆 gene(abcdefg)와 교환:       
                            1234567 abcdefg
                            -> abc4567 123defg
                            연산 불가능한 gene이 있다면 다시 원상복귀
                            
buildDeicsionTree 이후
       저장된 나무에 data를 test 데이터로 적용하여 fit
              모든 노드마다 저장된 rule에 데이터 하나하나 적용해보며 해당 노드에 속해있는지 검사하는 방식이라
              계산 시간 오래 걸리는 부분
              
visualizing
       노드 이름으로 부모/자식노드를 연결하는 방식

       
       
"""

"""
주로 발생하는 에러 1.
TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'

데이터 별로 unit을 불러오는 함수가 다름
MAPSDT > preprocessingData (line: 30) > get_???_unit (line: 46)에서 데이터에 맞게 수정

--------------------------------------------------------------------------------------

주로 발생하는 에러 2.
간혹 연속/범주형 변수를 나누는 기준 (unique value의 수)으로 인해 발생

functions.py > processContinuousFeatures (line: 20)에서 숫자 조정
data_load > attribute_set (line: 136)에서 숫자 조정
"""       
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





