import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import load

from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score

import warnings
warnings.filterwarnings("ignore")

def run(outputPrefix, modelName):
  model = load(f'data/{modelName}')
  df = pd.read_csv(f'data/{outputPrefix}_Comments.csv')

  X = df.drop(columns=['Raw Score'])
  Y = df['Raw Score']

  score = model.score(X, Y)
  print('Model score:', score)

  # Root Mean Squared Error on train and test data
  predictions = model.predict(X)
  print('RMSE on train data: ',  mean_squared_error(Y, predictions)**(0.5))
  print('R2 on train data: ',  r2_score(Y, predictions)**(0.5))

  # Plot predictions
  plt.figure()
  sns.distplot(predictions, label='Predictions')
  sns.distplot(Y, label='Real Values')
  plt.xlabel('')
  plt.legend()
  plt.title('Model Predictions vs Real Values')
  plt.show()

  plt.figure()
  plt.scatter(predictions, Y, marker='+', alpha=0.25)
  plt.title('Model Predictions vs Real Values')
  plt.xlabel('Predictions')
  plt.ylabel('Real Values')
  plt.show()

  # Save predicted csv
  df['AI Predicted Score'] = predictions
  df['Intelligent Adjusted Score'] = (df['Raw Score'] + df['AI Predicted Score']) / 2
  df.to_csv(f'data/{outputPrefix}_Results.csv', index=False)

if __name__ == '__main__':
  run(*sys.argv[1:])