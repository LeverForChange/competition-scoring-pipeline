import pandas as pd
import sys

def run(df):
  df = df[[
    'ID', 
    'Judge', 
    'Raw Score', 
    'AI Predicted Score', 
    'Intelligent Adjusted Score', 
    'Normalized Score'
    ]]
  grouped = df.groupby(['ID', 'Judge']).mean().groupby('ID')
  lowestDropped = (grouped.sum()['Raw Score'] - grouped['Raw Score'].agg('min')) / (grouped['Raw Score'].size() - 1)
  lowestDropped = lowestDropped.to_frame().reset_index().rename(columns={'Raw Score': 'Lowest Dropped Score'})

  namesGrouped = df.groupby('ID', as_index=False).agg({'ID': 'first'})
  df = pd.merge(namesGrouped, df.drop(labels="Judge", axis=1).groupby('ID').mean(), on='ID')
  df = pd.merge(df, lowestDropped, on='ID')

  df['Raw Rank'] = df.rank(method='min', ascending=False)['Raw Score'].astype(int)
  df['Normalized Rank'] = df.rank(method='min', ascending=False)['Normalized Score'].astype(int)
  df['Intelligent Adjusted Rank'] = df.rank(method='min', ascending=False)['Intelligent Adjusted Score'].astype(int)
  df['Lowest Dropped Rank'] = df.rank(method='min', ascending=False)['Lowest Dropped Score'].astype(int)
  return df