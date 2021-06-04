# Build the drug link graph in Python
This project is about building a data pipeline in order to generate a link graph between drugs and their mention in different scientific publications or clinical trials. 
The aim is to generate this graph in a json file format.

There are four input files which are available in the input directory: 
- drug.csv
- clinical_trials.csv
- pubmed.csv
- pubmed.json

##### Rules :
- A drug is considered as mentionned in a pubmed if the drug name is retrieved in the title of the publication. 
- A drug is considered as mentionned in a journal if it is quoted in the publication of this journal.

An example of this json file is available in the output directory
##### Contributor : 
Only I was working on this project



