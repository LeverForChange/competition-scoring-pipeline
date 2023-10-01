# General Instructions

1. Run `pip3 install -e .`. If you expect dependency conflicts to arise, it may be wise to activate a Python virtual environment first.
2. The NLP tasks require some external datasets to be downloaded on the local machine. 
  - Run the following command in your terminal: `python -m textblob.download_corpora`. If you encounter issues, consult: https://stackoverflow.com/questions/41310885/error-downloading-textblob-certificate-verify-failed
  - Then, open a python instance and run: `import nltk`, then `nltk.download('stopwords')`, then `nltk.download('omw-1.4')`. If you have problems, consult here: https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
  - If more problems persist, you may need to download nltk corpora "al la carte". Follow the python shell commands outputted in red by nltk.

# Setup config file

`cp config.py.tmpl config.py`

And then edit it, filling in the various parts that you are using.  The `TRAINING` sections should be used for GlobalView, while the SCORING sections are for the specific competition.

# Competition Scoring Pipeline

Example command: `python scoringPipeline.py /path/to/model.joblib`

The scoring pipeline will apply the trained model to predict judge scores for a given set of scoring data.

The first argument is the name of the model file to run score the input proposals with.

# Model Building (Training) Pipeline

Example command: `python trainingPipeline.py /path/to/model.joblib`

You may want to re-train the model for a number of reasons - adding new fields, changing parameters, tweaking the NLP approach, or simply because new proposals/cleaned/refactored data have been entered into Torque. This pipeline will build the pipeline needed for predicting intelligent scores for LFC competitions.

# Using from other python code

Look at `./trainingPipeline.py` and `./scoringPipeline.py` to see how they build up a torque instance and call into the module.
