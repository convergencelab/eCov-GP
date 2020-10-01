# eCov-GP


*NOTE* all this is working on linux. I had difficulty in the past with windows getting pygraphviz working right. If you're on windows and it doesn't work, it will only impact 1 single function in the eCov-results script (draw_tree). 

1. Use Anaconda distro of Python --- https://www.anaconda.com/products/individual
2. Create a conda environment for DEAP (important so you don't destroy your Python install) --- https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#viewing-a-list-of-your-environments
3. Using conda (conda install X), get:
-- numpy
-- scipy
-- scikit-learn
-- matplotlib
-- networkx
-- tqdm

4. Using pip install, get:
-- deap
-- ndlib
-- scoop

5. Add subfolders to wherever you download the code to:
-- output
-- function_tests

6. Get pygraphviz installed using this info --- https://anaconda.org/conda-forge/pygraphviz
*NOTE* I do not know if this works on windows, but I can confirm that it does on linux. 

How to use the code:
- eCov-GP is the one that runs the evolutionary search for results. I suggest using populations and generations of 200 -- 500 (for both). Feel free to play with the parameters to see what happens. 
- eCov-results is the script that lets us look at our results and see what we get. Note that I fixed the code on github so the diffusion trend function works.
- Once you find something you like, look at the resulting function and simplify it to something you can code up as an actual python function. 
- Add the function to the strategies script
- Feel free to do big tests of your new strategies with the eCov-test script. 
