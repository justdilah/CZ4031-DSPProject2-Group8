# CZ4031-DSPProject2-Group8
Project 2 Implementation for CZ4031 DATABASE SYSTEM PRINCIPLES

**Before running the code:**
- go to config.json and edit "pwd" to the master password you have set when setting up PostgreSQL

**Libraries Installation:**
- pip install pyqt5
- pip install pyqt5-tools
- pip install psycopg2
- pip install qt-material
- pip install gTTS
- pip install networkx
- pip install matplotlib
- pip install scipy


## How to use Explain Class
---
```python
# Instantiate cursorManager
# Instantiate UI
# Instantiate Explain class
cursorManager = CursorManager()
explain = Explain(ui, cursorManager)

# Build QEP tree by passing in the query as param
# Returns the root node of the QEP tree
QEPtree1 = explain.build_qep_tree(query1)
QEPtree2 = explain.build_qep_tree(query2)

# Get explanation for specified query (q1 or q2) by passing in
# the root node of the respective QEP tree
# Returns List[str] of explanations
explanation = explain.get_QEP_explanation(QEPtree1)

# Get the comparisons between 2 QEP
# by passing the 2 QEPtrees as params
# Returns List[str] of comparisons between the 2 QEPs
comparison = explain.get_QEP_comparison(QEPtree1, QEPtree2)

# Get visual plan of specified QEP 
# by passing in the respective QEPtree that we want the visual plan for
# Returns List[str] representation of the tree
visualPlan = explain.get_visual_plan(QEPtree1)
```
