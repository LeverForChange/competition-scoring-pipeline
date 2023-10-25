#!/usr/bin/env python

from distutils.core import setup

setup(
    name="competition_scoring_pipeline",
    version="0.1.0",
    description="Training and Scoring for competitions at Lever for Change",
    author="Lever for Change",
    author_email="intentionally@left.blank.com",
    url="https://github.com/LeverForChange/competition-scoring-pipeline",
    packages=["competition_scoring_pipeline"],
    install_requires=["pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "joblib", "textstat", "nltk", "textblob", "torqueclient"]
)
