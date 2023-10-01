import sys
import argparse

import submittableConverter
import textAnalyzer
import predictor
import normalizer
import ranker

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', type=str, help='Name of downloaded results file placed in the data/ directory')
  parser.add_argument('outputPrefix', type=str, help='Prefix to distinguish output files')
  parser.add_argument('modelName', type=str, help='Name of the model to use, including the .joblib extension')
  args = parser.parse_args()
  
  # Convert Submittable file download to Torque format
  print('Converting from Submittable file...')
  submittableConverter.run(args.filename, args.outputPrefix)

  # Create text metrics from comments
  print('Analyzing comment text...')
  textAnalyzer.run(args.outputPrefix)

  # Predictor intelligent scores
  print('Predicting scores...')
  predictor.run(args.outputPrefix, args.modelName)

  # Normalize scores
  print('Normalizing scores...')
  normalizer.run(args.outputPrefix)

  # Create final rankings + calculate lowest scores dropped
  print('Ranking proposals')
  ranker.run(args.outputPrefix)

  print(f'Ranked proposals output in data/{args.outputPrefix}_Ranked.csv')