# iM-Seeker

iM-Seeker is commandline software designed to predict DNA i-Motif folding status and folding strength.
Details can be found at https://github.com/YANGB1/iM-Seeker

# Installation and Usage
The dependency packages can be installed by:
``` 
pip3 install -r requirements.txt
``` 
iM-Seeker can be installed by:
``` 
pip3 install iM-Seeker
```
Alternatively, the python script 'iM-Seeker.py' can be downloaded directly from Github. The stored directory can be added to the ‘PATH’ environmental variable or the scripts with full path can be run alternatively using command like: 
``` 
python3 iM-Seeker.py -h
``` 
**Please pay attention !!!!!! The program needs two models 'pickle_model_classification.pkl' and 'pickle_model_regression.pkl' which are required as the input files of the software. Please find all the files at https://figshare.com/s/e4e72e2e8ceaa0a4fbd6, where all these files can be downloaded directly.**
  
After intalled the package with 'pip',the help page can be checked by following command:
``` 
iM-Seeker.py -h
``` 
Parameters can be configured according to the user's own needs. Here is an example:
``` 
iM-Seeker.py --sequence input.fa --classification_model pickle_model_classification.pkl --regression_model pickle_model_regression.pkl --overlapped 2 --greedy 2 --stem_short 3 --stem_long 5 --loop1_short 1 --loop1_long 12 --loop2_short 1 --loop2_long 12 --loop3_short 1 --loop3_long 12 --representative_conformation 2 --output_folder output_path
``` 

# Input and output
The input sequences should be in fasta formation, for instance:

\>test1

CCCTCCCCCTCCCCTCCCTCCCCCCCCTCCCCTCCCTCCCTCCCCCCCCTCCCTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTCCCCCCCCCTCCTCCCCTCCCCCTCCCCTCCCTCCCTCC

\>test2

CCCCCTCCCCCTCCCCCTCCCCCTCCCCC

\>test3

CCCTAACCCTAACCCTAACCCTAACCCTAACCCTAACCC

\>test4

CCCCGACCCCAACCCCTCCCCCAACCCCTCCCC

The output files are stored in the pre-set output folder.

If --representative_conformation is set as 1, 'iM-seeker_result_average_conformation.txt' includes conformation A of pre-set iM structures. 

If --representative_conformation is set as 2, 'iM-seeker_result_side_shorter_conformation.txt' includes conformation B of pre-set iM structures. 

The prediction result is kept in 'iM-seeker_final_prediction.txt'.

"0" of folding status means unfolded while "1" means folded. Folding strength is a continuous number. 