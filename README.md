# General Instructions

1. Run `pip install -r requirements.txt`. If you expect dependency conflicts to arise, it may be wise to activate a Python virtual environment first.
2. The NLP tasks require some external datasets to be downloaded on the local machine. 
  - Run the following command in your terminal: `python -m textblob.download_corpora`. If you encounter issues, consult: https://stackoverflow.com/questions/41310885/error-downloading-textblob-certificate-verify-failed
  - Then, open a python instance and run: `import nltk`, then `nltk.download('stopwords')`, then `nltk.download('omw-1.4')`. If you have problems, consult here: https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
  - If more problems persist, you may need to download nltk corpora "al la carte". Follow the python shell commands outputted in red by nltk.

# Competition Scoring Pipeline

Example command: `python scoring_pipeline.py submittable_download.csv BAWOP LFC_model.joblib`

The scoring pipeline will apply the trained model to predict judge scores for a given set of scoring data. The pipeline is geared to clean data coming from the BAWOP challenge using Submittable as the vendor. You'd need to eliminate/refactor this step for data downloaded from Torque or another vendor. 

The first argument is simply the name of the downloaded data file. Make sure it's in a `data/` subdirectory from the root of this project. 

The second argument is simply a parameter used to prefix outputted data files. The final dataset with ranked and normalized scores for each proposal will be named `PREFIX_RANKED.csv`. The other output files may be useful for exploratory analyses.

### Note on downloading Submittable data

The data coming from Submittable may have slight incosistencies, which would require altering `submittable_converter.py`. For example, the names of the criteria categories may change, and the column titles may not be consistent across all criteria categories. Downloads from the reporting dashboard may also include a meaningless filler row at the top. In sum, it's imperative to visual check the raw data download before running through the pipeline.

# Model Building (Training) Pipeline

Example command: `python trainingPipeline.py lfc-proposals.csv MY_MODEL`

You may want to re-train the model for a number of reasons - adding new fields, changing parameters, tweaking the NLP approach, or simply because new proposals/cleaned/refactored data have been entered into Torque. This pipeline will build the pipeline needed for predicting intelligent scores for LFC competitions.

You'll need to download data from GlobalView to train the model on, see below for the minimum set of required fields.

### Required Columns for Pipeline

The following columns are required for downloaded CSV from Global View for building new intelligent scoring models:

```
"Application #",
"Competition Name",
"Project Title",
"Organization Name",
"Panel DURABLE Judge Data",
"Panel SUSTAINABLE Judge Data",
"Panel EVIDENCE-BASED Judge Data",
"Panel FEASIBLE Judge Data",
"Panel IMPACTFUL Judge Data",
"Panel COMMUNITY-INFORMED Judge Data",
"Panel COMMUNITY CENTERED Judge Data",
"Panel SCALABLE Judge Data",
"Panel EQUITABLE Judge Data",
"Panel ACTIONABLE Judge Data",
"Panel BOLD Judge Data",
"Panel INNOVATIVE Judge Data",
"Panel TRANSFORMATIVE Judge Data"
```
