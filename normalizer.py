import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys

def run(df):
  df['Temp_ID'] = df['ID'] + df['Criteria']

  mu = df['Raw Score'].mean()
  gamma = df[['Raw Score', 'Judge']].groupby('Judge').std()
  alpha = df[['Raw Score', 'Judge']].groupby('Judge').mean() - mu
  beta = df[['Raw Score', 'Temp_ID']].groupby('Temp_ID').mean() - mu

  # estimate = mu + gamma_i * (alpha_i   + beta_j)
  estimates = []
  for index, row in df.iterrows():
    gamma_i = gamma.at[row.Judge, 'Raw Score']
    alpha_i = alpha.at[row.Judge, 'Raw Score']
    beta_j = beta.at[row.Temp_ID, 'Raw Score']
    estimate = mu + (gamma_i * (alpha_i + beta_j))
    estimates.append(estimate)
  df['Normalized Score'] = estimates
  
  df.drop(columns='Temp_ID', inplace=True)

  plt.figure()
  sns.distplot(df['Normalized Score'])
  sns.distplot(df['Raw Score'])
  plt.show()

  return df

if __name__ == '__main__':
  run(*sys.argv)