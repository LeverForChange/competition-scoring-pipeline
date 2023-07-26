import sys
import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer

def run(df):
  # Select train x, y data + split
  X = df.drop(columns=['Raw Score'])
  Y = df['Raw Score']

  numeric_cols = [
    'Word Count', 'Char Count', 'Sentence Count',
    'Avg Word', 'Sentiment', 'Sent Neu', 'Sent Pos', 'Sent Neg',
    'Stopwords', 'Complexity'
    ]
  numeric_transformer = Pipeline(steps=[
    ('impute', SimpleImputer(strategy='mean')),
    ('scale', StandardScaler())
    ],
    verbose=True
    )

  cat_transformer = Pipeline(steps=[
    ('encode_criteria', OneHotEncoder(sparse=False)),
    ],
    verbose=True
    )
  cat_cols = ['Criteria']

  text_transformer = TfidfVectorizer(ngram_range=(1,3))

  preprocess = ColumnTransformer(
    remainder='drop',
    transformers=[
      ('tfidf', text_transformer, 'Text'),
      ('numeric', numeric_transformer, numeric_cols),
      ('categorical', cat_transformer, cat_cols),
      ],
    verbose=True
    )

  estimator = linear_model.Ridge()

  pipeline = Pipeline(steps=[
    ('transformer', preprocess),
    ('estimator', estimator)
    ],
    verbose=True
    )
  return pipeline.fit(X, Y)

if __name__ == '__main__':
  run(*sys.argv[1:])