# Coursework 1  : a simple IR tool

SNN: s1956340

These instructions are written for running this coursework project.

##  1. Environment and packages

I completed this project using my personal computer with **macOS**.Hopefully, there will not occur any problems in other systems.

The python version is **Python 3.7.4**, using anaconda as the environment manager.

To run this project, below **packages** are compulsory.

- nltk.stem
- xml.etree.ElementTree
- collections 
- numpy
- re

## 2. Prepare data before running

It's necessary to make sure existing the data in the right folder before running.(or you can also change the data path by hand)

- **data_documents/:** 

  Put the **stop words file 'englishST.txt'** and the **collection file 'trec.5000.xml'** in this folder.

  (Here I kept the stop words file in this folder.)

- **assign_output/, lab_output/:**

  Get the assign or lab output file: index.txt; results.boolean.txt; results.ranked.txt

  (Here I kept the assignment **index.txt**.)

- **query/:**

  Put the queries file in this folder for both lab and assignment.

  (Here I kept the assignment boolean and ranked queries. )

#### Easy start about data:

1. Because we are not allowed to submit the collection file with code.For retraining the 'index.txt', just put  'trec.5000.xml' into 'data_documents' folder. 

   **NOTE:**  Add header <roots> and footer </roots> to the file to make it parsable by xml.etree.ElementTree library!!! Or it will occur an error.

2. If just for searching, needn't do any change with the data.

## 3. Running step

I write 4 python files in this project. Making three of them as my own packages. So just using 'main.py' to run the project is enough.

1. Make sure you have prepare the environment and data as I mentioned above.
2. run the python file 'main.py' to do the search
3. if you want to retrain the index file, delete the annotation about this part in the 'main.py'





