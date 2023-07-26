"""
#1 Impactful
#2 Feasible
#3 Community Centered
#4 Sustainable
Review 1: #1 Impactful - Reviewer Comments: (Round 2 (a) - Evaluation Panel)
Review 1: #1 Impactful (1-5): Score (Round 2 (a) - Evaluation Panel)
Review 1: Reviewer Email (Round 2 (a) - Evaluation Panel)
Review 1: What is your overall impression of this submission? Please use this space to provide any general thoughts about the application as a whole. (Round 2 (a) - Evaluation Panel)
"""

import pandas as pd
import numpy as np
import sys
import config

def run(torque):
  reviewers = range(1, 6)
  df = []

  for proposal in torque.competitions[config.SCORING_TORQUE_COMPETITION].proposals:
    for judge_data_type in config.SCORING_JUDGE_DATA_TYPES:
      if proposal["%s %s Judge Data" % (config.SCORING_SCORE_TYPE, judge_data_type)]:
        for torque_judge_datum in proposal["%s %s Judge Data" % (config.SCORING_SCORE_TYPE, judge_data_type)]["Comments"]:
          if (not torque_judge_datum.get('Comment') or 
              not torque_judge_datum.get('Score', {}).get('Raw') or 
              not torque_judge_datum.get('Anonymous Judge Name')):
            continue

          judge = torque_judge_datum["Anonymous Judge Name"]
          score = torque_judge_datum["Score"]["Raw"]
          comment = torque_judge_datum["Comment"]
          eval = {
            'ID': proposal["Application #"],
            'Comment': comment,
            'Criteria': judge_data_type,
            'Raw Score': float(score),
            'Judge': judge
          }
          df.append(eval)

  return pd.DataFrame.from_records(df)

if __name__ == '__main__':
  run(*sys.argv[1:])