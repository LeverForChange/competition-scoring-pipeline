import argparse

import commentExtractor
import textAnalyzer
import modelBuilder
import predictor
import config

from joblib import dump
from torqueclient import Torque

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

if __name__ == '__main__':
  import config
  torque = Torque(
      config.TRAINING_TORQUE_LINK,
      config.TRAINING_TORQUE_USERNAME,
      config.TRAINING_TORQUE_API_KEY
  )

  parser = argparse.ArgumentParser()
  parser.add_argument('outputFile', type=str, help='Output file location')
  args = parser.parse_args()

  run(torque, args.outputFile)