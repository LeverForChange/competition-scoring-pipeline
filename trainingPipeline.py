import argparse

import commentExtractor
import textAnalyzer
import modelBuilder
import predictor

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('filename', type=str, help='Name of downloaded results file placed in the data/ directory')
  parser.add_argument('outputPrefix', type=str, help='Prefix to distinguish output files')
  args = parser.parse_args()
  
  # Reformat Global View download by extracting comments
  print('Extracting comments...')
  commentExtractor.run(args.filename, args.outputPrefix)

  # Create text metrics from comments
  print('Analyzing comment text...')
  textAnalyzer.run(args.outputPrefix)

  # Predictor intelligent scores
  print('Predicting scores...')
  modelBuilder.run(args.outputPrefix)
  print(f'Your model was successfuly built to data/{args.outputPrefix}_model.joblib')
  
  # Score/visualize model
  print('Scoring model...')
  predictor.run(args.outputPrefix, f'{args.outputPrefix}_model.joblib')
  