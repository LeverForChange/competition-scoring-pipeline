import pandas as pd
import textstat
import sys

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from textblob import Word

stop = stopwords.words('english')

def cleanText(series):
  cleaned = series.apply(lambda x: x.lower() if isinstance(x, str) else '')
  cleaned = cleaned.str.replace('[^\w\s]', '')
  cleaned = cleaned.apply(lambda x: ' '.join(x for x in x.split() if x not in stop))
  cleaned = cleaned.apply(lambda x: ' '.join([Word(word).lemmatize() for word in x.split()]))
  return cleaned

def avg_word(sentence):
  words = sentence.split()
  return (sum(len(word) for word in words)/len(words))

def run(df):
  stop = stopwords.words('english')
  sid = SentimentIntensityAnalyzer()

  df['Text'] = cleanText(df.Comment)
  df['Comment'] = df['Comment'].astype(str)

  # Char/word count
  df['Word Count'] = df.Comment.apply(lambda x: textstat.lexicon_count(x))
  df['Char Count'] = df.Comment.apply(lambda x: len(x))
  df['Sentence Count'] = df.Comment.apply(lambda x: textstat.sentence_count(x))
  df['Avg Word'] = df.Comment.apply(lambda x: avg_word(x))

  # Stopwords
  df['Stopwords'] = df.Comment.apply(lambda x: len([x for x in x.split() if x in stop]))

  # Apply sentiment scores to comment
  sentiments = df.Text.apply(lambda c: sid.polarity_scores(c))
  df['Sentiment'] = sentiments.apply(lambda s: s['compound'])
  df['Sent Neg'] = sentiments.apply(lambda s: s['neg'])
  df['Sent Pos'] = sentiments.apply(lambda s: s['pos'])
  df['Sent Neu'] = sentiments.apply(lambda s: s['neu'])

  # Comment complexity
  df['Complexity'] = df.Comment.apply(lambda x: textstat.flesch_reading_ease(x))

  df.dropna(inplace=True)
  return df
