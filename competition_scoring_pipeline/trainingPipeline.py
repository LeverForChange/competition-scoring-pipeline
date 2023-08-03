import argparse

from competition_scoring_pipeline import commentExtractor, textAnalyzer, modelBuilder, predictor

from joblib import dump

def run(torque, outputFile):
  # Reformat Global View download by extracting comments
  print('Extracting comments...')
  comment_dataframe = commentExtractor.run(torque)

  # Create text metrics from comments
  print('Analyzing comment text...')
  analyzed_dataframe = textAnalyzer.run(comment_dataframe)

  # Predictor intelligent scores
  print('Predicting scores...')
  model = modelBuilder.run(analyzed_dataframe)
  dump(model, outputFile)
  print(f'Your model was successfuly built to {outputFile}')