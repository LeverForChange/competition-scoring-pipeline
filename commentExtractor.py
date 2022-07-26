import pandas as pd
import json
import sys


def run(inputFile, outputPrefix):
  df = []

  # Read in CSV data and select criteria columns
  proposals = pd.read_csv(f'data/{inputFile}')
  raw = proposals.filter(regex='Panel\s[A-Z\-]+\sJudge\sData')
  competitions = proposals['Competition Name']

  # For each comment in the criteria data, add a row to new dataframe
  for col, series in raw.iteritems():
    for i, row in enumerate(series):
      try:
        row = json.loads(row)
      except:
        continue
      if not row:
        continue

      # Extract comments/scores/judge ID
      comments = []
      scores = []
      judges = []
      for r in row.get('Comments'):
        if (not r.get('Comment') or 
            not r.get('Score', {}).get('Raw') or 
            not r.get('Anonymous Judge Name')):
          continue
        comments.append(r['Comment'])
        scores.append(r['Score']['Raw'])
        judges.append(r['Anonymous Judge Name'].split(' ')[-1])

      # Criteria word
      criteria = col.split(' ')[1]
      criteria = [criteria] * len(comments)

      # Select competition
      comp = competitions.iloc[i]
      competition = [comp] * len(comments)

      # Get other proposal data
      prop = proposals.iloc[i]
      appIds = [
          f"{prop['Competition Name']}_{prop['Application #']}"
          ] * len(comments)

      # Add new rows to our Data Frame
      df.extend(list(zip(
          appIds,
          comments,
          criteria,
          scores,
          competition,
          judges
      )))

  df = pd.DataFrame(
    df,
    columns=[
      'ID',
      'Comment',
      'Criteria',
      'Raw Score',
      'Competition',
      'Judge'
    ]
  )
  df.dropna(subset=['Comment', 'Raw Score', 'Judge'], inplace=True)
  df.to_csv(f'data/{outputPrefix}_Comments.csv', index=False)

if __name__ == '__main__':
  run(*sys.argv[1:])
