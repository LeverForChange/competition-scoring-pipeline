import argparse
import config

from torqueclient import Torque
from competition_scoring_pipeline import scoringPipeline

if __name__ == '__main__':
  torque = Torque(
    config.SCORING_TORQUE_LINK,
    config.SCORING_TORQUE_USERNAME,
    config.SCORING_TORQUE_API_KEY
  )

  parser = argparse.ArgumentParser()
  parser.add_argument('modelName', type=str, help='Name of the model to use, including the .joblib extension')
  args = parser.parse_args()
  scoringPipeline.run(
    torque,
    args.modelName,
    config.SCORING_TORQUE_COMPETITION,
    config.SCORING_SCORE_TYPE,
    config.SCORING_JUDGE_DATA_TYPES
  )
