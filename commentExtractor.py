import pandas as pd
import json
import sys
import config
import re

def run(torque):
  df = []

  # For each comment in the criteria data, add a row to new dataframe
  for competition in torque.competitions:
      for proposal in competition.proposals:
        appId = f"{proposal['Competition Name']}_{proposal['Application #']}"

        for key in proposal.keys():
          if re.match('Panel\s[A-Z\-]+\sJudge\sData', key):
            if not proposal[key]:
              continue

            for comment in proposal[key].get("Comments", []):
              if (not comment.get('Comment') or 
                  not comment.get('Score', {}).get('Raw') or 
                  not comment.get('Anonymous Judge Name')):
                continue

              df.append([
                appId,
                comment["Comment"],
                key.split(' ')[1],
                float(comment["Score"]["Raw"]),
                proposal["Competition Name"],
                comment["Anonymous Judge Name"].split(' ')[-1],
              ])

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
  return df

if __name__ == '__main__':
  run(*sys.argv[1:])
