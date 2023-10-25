from competition_scoring_pipeline import torqueConverter, textAnalyzer, predictor, normalizer, ranker
from joblib import load

def run(torque, modelName, competition, score_type, judge_data_types, column_mapping={}):
  # Convert Submittable file download to Torque format
  print('Getting scores from torque...')
  torque.bulk_fetch(torque.competitions[competition].proposals)
  comment_df = torqueConverter.run(torque.competitions[competition].proposals, score_type, judge_data_types, column_mapping=column_mapping)

  # Create text metrics from comments
  print('Analyzing comment text...')
  analyzed_dataframe = textAnalyzer.run(comment_df)
  model = load(modelName)

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
    current_rank = torque.competitions[competition].proposals[record["ID"]]["%s Rank" % score_type]
    current_score = torque.competitions[competition].proposals[record["ID"]]["%s Score" % score_type]

    current_rank["LFC Intelligent Adjusted"] = record["Intelligent Adjusted Rank"]
    current_score["LFC Intelligent Adjusted"] = round(record["Intelligent Adjusted Score"] * 20, 1)
    current_rank["LFC Normalized"] = record["Normalized Rank"]
    current_score["LFC Normalized"] = round(record["Normalized Score"] * 20, 1)
    current_rank["LFC Lowest Dropped"] = record["Lowest Dropped Rank"]
    current_score["LFC Lowest Dropped"] = round(record["Lowest Dropped Score"] * 20, 1)

    torque.competitions[competition].proposals[record["ID"]]["%s Rank" % score_type] = current_rank
    torque.competitions[competition].proposals[record["ID"]]["%s Score" % score_type] = current_score

def run_in_memory(proposals, modelName, score_type, judge_data_types, column_mapping={}):
  comment_df = torqueConverter.run(proposals, score_type, judge_data_types, column_mapping=column_mapping)
  analyzed_dataframe = textAnalyzer.run(comment_df)
  model = load(modelName)
  predicted_dataframe = predictor.run(model, analyzed_dataframe)
  normalized_dataframe = normalizer.run(predicted_dataframe)
  ranked_dataframe = ranker.run(normalized_dataframe)

  resp = {}
  for record in ranked_dataframe.to_dict(orient='records'):
    resp[record["ID"]] = {
      "%s Rank" % score_type: {
        "LFC Intelligent Adjusted": record["Intelligent Adjusted Rank"],
        "LFC Normalized": record["Normalized Rank"],
        "LFC Lowest Dropped": record["Lowest Dropped Rank"],
      },
      "%s Score" % score_type: {
        "LFC Intelligent Adjusted": round(record["Intelligent Adjusted Score"] * 20, 1),
        "LFC Normalized": round(record["Normalized Score"] * 20, 1),
        "LFC Lowest Dropped": round(record["Lowest Dropped Score"] * 20, 1),
      },
      "Judge Scores": {}
    }

  for record in normalized_dataframe.to_dict(orient='records'):
    inverted_column_mapping = {c[1]: c[0] for c in column_mapping.items()}
    criteria = record["Criteria"]
    criteria = inverted_column_mapping.get(criteria, criteria)
    judge = record["Judge"]
    if criteria not in resp[record["ID"]]["Judge Scores"]:
      resp[record["ID"]]["Judge Scores"][criteria] = {}

    resp[record["ID"]]["Judge Scores"][criteria][judge] = {
      "LFC Intelligent Adjusted": round(record["Intelligent Adjusted Score"], 1),
      "LFC Normalized": round(record["Normalized Score"], 1),
    }

  return resp