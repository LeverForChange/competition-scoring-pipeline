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

def run(filename, outputPrefix):

  evals = pd.read_csv(f'data/{filename}')
  evals = evals[evals['Review Stage (Form Attributes)'] == 'Round 2 (a) - Evaluation Panel']

  criterias = ['#1 Impactful', '#2 Feasible', '#3 Community Centered', '#4 Sustainable']
  reviewers = range(1, 6)
  nulls = ['(blank)', '', None, np.nan]
  proposalCol = 'Project Title  (Section B. Application: Build A World of Play Challenge)'
  orgCol = 'Lead Organization Legal Name: (Section B. Application: Build A World of Play Challenge)'
  df = []

  for index, row in evals.iterrows():
    proposalId = row[proposalCol]
    organization = row[orgCol]
    for review in reviewers:
      judgeCol = f'Review {review}: Reviewer Email (Round 2 (a) - Evaluation Panel)'
      judge = row[judgeCol]
      for criteria in criterias:
        # The Sustainable column has as slightly different format for some reason
        if 'Sustainable' in criteria:
          scoreCol = f'Review {review}: {criteria} : Score (Round 2 (a) - Evaluation Panel)'
        else:
          scoreCol = f'Review {review}: {criteria} (1-5): Score (Round 2 (a) - Evaluation Panel)'
        commentCol = f'Review {review}: {criteria} - Reviewer Comments: (Round 2 (a) - Evaluation Panel)'
        try:
          score = row[scoreCol]
          comment = row[commentCol]
          if comment in nulls:
            comment = 'NO COMMENT'
        except KeyError as e:
          continue
        # Convert criteria to align with Torque vocabulary
        criteria = criteria.replace('Sustainable', 'Durable')
        criteria = criteria.replace('Community Centered', 'Community-Informed')
        eval = {
          'ID': f'Lego_{index}',
          'Proposal': proposalId,
          'Organization': organization,
          'Comment': comment,
          'Criteria': criteria.split(' ')[1].upper(),
          'Raw Score': score,
          'Competition': 'Lego',
          'Judge': judge
        }
        if not score in nulls:
          df.append(eval)
        else:
          print(f'WARNING: missing score at {proposalId}')

  df = pd.DataFrame.from_records(df)
  df.to_csv(f'data/{outputPrefix}_Comments.csv', index=False)

if __name__ == '__main__':
  run(*sys.argv[1:])