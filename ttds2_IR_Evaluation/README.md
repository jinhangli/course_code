# Coursework 2 part.a  : **IR Evaluation**

SNN: s1956340

These instructions are written for running this coursework project on part a, IR evaluation.

##  1. Environment and packages

I completed this project using my personal computer with **macOS**.Hopefully, there will not occur any problems in other systems.

The python version is **Python 3.7.4**, using anaconda as the environment manager.

To run this project, below **packages** are compulsory.

- os
- re
- collections 
- numpy
- scipy.stats

## 2. Data

- **systems/:** 

  The input data to run the evaluation: 

  - **S[1-6].results** : information retrieval results from 6 different IR systems

  - **qrels.txt**：file which contains the list of relevant documents for each of the 10 queries

- **output/:**

  Run the python file **evaluation.py**, we can get below files:

  - **S[1-6].eval**: 6 files for each of the 6 systems, named from S1.eval to S6.eval

    Each file should contain a table of the above scores for each of the 10 queries

  - **All.eval**: the average scores of each of the 6 systems

- **evaluation.py**

  Run the file to get the evaluation results, storing in the output folder

- **t_test.py**

  Using 2-tailed t-test, with p-value of 0.05, to find out if the system is statistically significantly better than the second system

## 3. Running step

1. Make sure you have prepare the environment and data as I mentioned above.
2. Run the python file **'evaluation.py'** to do the evaluation.
3. Run the python file **'t_test.py'** to do the t-test, calculating the p-value.



