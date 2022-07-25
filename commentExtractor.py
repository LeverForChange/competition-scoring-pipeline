import pandas as pd
import json
import sys


def run(inputFile, outputPrefix):
  df = []

  # Read in CSV data and select criteria columns
  proposals = pd.read_csv(f'data/{inputFile}')
  raw = proposals.filter(regex='Panel\s[A-Z\-]+\sJudge\sData')
  competitions = proposals['Competition Domain']

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
      row = row.get('Comments')
      comments = [r['Comment'] for r in row]
      scores = [r['Score']['Raw'] for r in row]
      judges = [r.get('Anonymous Judge Name', r.get('Judge Email')) for r in row]
      judges = list(map(lambda x: x.split(' ')[-1], judges))

      # Criteria word
      criteria = col.split(' ')[1]
      criteria = [criteria] * len(comments)

      # Select competition
      comp = competitions.iloc[i]
      competition = [comp] * len(comments)

      # Get other proposal data
      prop = proposals.iloc[i]
      appIds = [
          f"{prop['Competition Domain']}_{prop['Application #']}"] * len(comments)

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
