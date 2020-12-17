#!/bin/bash
#SBATCH --account=def-jhughe54
#SBATCH --time=4-0
#SBATCH --mem-per-cpu=10M
#SBATCH --job-name=eCovid-GP
# These are commented out for initial testing 
# SBATCH --output=/dev/null 
# SBATCH --error=/dev/null [...]
#SBATCH --array=1-10

# Need Python 3.8
module load StdEnv/2020 igraph/0.8.2 python/3.8

# Load up DEAP virtual environment (switched to testndlib because it worked)
source ~/virtualEnvs/testndlib/bin/activate

# Need DEAP
# Need ndlib
# need networkx
# need tqdm
# need matplotlib

python eCov-GP-eval.py
