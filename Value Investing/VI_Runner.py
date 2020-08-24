#This is a python script that runs both the F-Scores and Magic-Formula python programs given a large
#dataset - This necessary to avoid complications found when attempting to run each program individually
#over the dataset.
import os

for runNum in range(0, 16):
    os.system("python3 magic_formula_revised.py " + str(runNum))