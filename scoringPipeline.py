import sys
import argparse

import torqueConverter
import textAnalyzer
import predictor
import normalizer
import ranker
import config

from torqueclient import Torque
from joblib import load

if __name__ == '__main__':
  torque = Torque(
      config.SCORING_TORQUE_LINK,
      config.SCORING_TORQUE_USERNAME,
      config.SCORING_TORQUE_API_KEY
  )

  parser = argparse.ArgumentParser()
  parser.add_argument('modelName', type=str, help='Name of the model to use, including the .joblib extension')
  args = parser.parse_args()
  
  # Convert Submittable file download to Torque format
  print('Getting scores from torque...')
  comment_df = torqueConverter.run(torque)

  # Create text metrics from comments
  print('Analyzing comment text...')
  analyzed_dataframe = textAnalyzer.run(comment_df)
  model = load(args.modelName)

  # Predictor intelligent scores
  print('Predicting scores...')
  predicted_dataframe = predictor.run(model, analyzed_dataframe)

  # Normalize scores
  print('Normalizing scores...')
  normalized_dataframe = normalizer.run(predicted_dataframe)

  # Create final rankings + calculate lowest scores dropped
  print('Ranking proposals')
  ranked_dataframe = ranker.run(normalized_dataframe)

  print('Saving data back to torque')
  for record in ranked_dataframe.to_dict(orient='records'):
      current_rank = torque.competitions[config.SCORING_TORQUE_COMPETITION].proposals[record["ID"]]["%s Rank" % config.SCORING_SCORE_TYPE]
      current_score = torque.competitions[config.SCORING_TORQUE_COMPETITION].proposals[record["ID"]]["%s Score" % config.SCORING_SCORE_TYPE]

      current_rank["LFC Intelligent Adjusted"] = record["Intelligent Adjusted Rank"]
      current_score["LFC Intelligent Adjusted"] = round(record["Intelligent Adjusted Score"] * 20, 1)
      current_rank["LFC Normalized"] = record["Normalized Rank"]
      current_score["LFC Normalized"] = round(record["Normalized Score"] * 20, 1)
      current_rank["LFC Lowest Dropped"] = record["Lowest Dropped Rank"]
      current_score["LFC Lowest Dropped"] = round(record["Lowest Dropped Score"] * 20, 1)

      torque.competitions[config.SCORING_TORQUE_COMPETITION].proposals[record["ID"]]["%s Rank" % config.SCORING_SCORE_TYPE] = current_rank
      torque.competitions[config.SCORING_TORQUE_COMPETITION].proposals[record["ID"]]["%s Score" % config.SCORING_SCORE_TYPE] = current_score