# Environment set up

### Miniconda ###

Within this course we will be using Python 3 along with a few open-source libraries (packages). First follow the instructions for **Installing Miniconda** from the [MLP course Environment set up 
notes](https://github.com/CSTR-Edinburgh/mlpractical/blob/mlp2019-20/lab1/notes/environment-set-up.md). If you already have Miniconda installed you can move to the next section.

### Conda environment ###

Create the Conda environment for the DME labs with:

```bash
conda create -n dme python=3
```

Type `y` when presented with the package plan. Every time you start working on the lab exercises you have to activate your environment with:

```bash
source activate dme
```

omitting "source" for a Windows installation. To deactivate the environment do: `source deactivate dme` (or ` deactivate dme` for Windows).

We will now install the required packages:

```bash
conda install jupyter numpy scipy matplotlib pandas statsmodels scikit-learn seaborn
conda install -c conda-forge scikit-optimize
```


### Course material ###

Once you have finished installed everything, you should download the course material from dme2020. 

Open a terminal (or Command Prompt in Windows), navigate to the folder where you have downloaded the course material and type:

  ```bash
  jupyter notebook
  ```

Then click on `01_Lab_1_Visualisation.ipynb` to open it.
