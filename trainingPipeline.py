import argparse
import config

from torqueclient import Torque
from competition_scoring_pipeline import trainingPipeline

if __name__ == '__main__':
  torque = Torque(
    config.TRAINING_TORQUE_LINK,
    config.TRAINING_TORQUE_USERNAME,
    config.TRAINING_TORQUE_API_KEY
  )

  parser = argparse.ArgumentParser()
  parser.add_argument('outputFile', type=str, help='Output file location')
  args = parser.parse_args()

  trainingPipeline.run(torque, args.outputFile)
