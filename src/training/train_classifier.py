import logging
from src.config import Config
from src.models.mineral_classifier import MineralClassifier

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Classifier Training...")
    config = Config.load()
    clf = MineralClassifier(config)
    clf.build()
    
    # TODO(person-2): Implement full training loop utilizing data loaders and config
    logger.info("Training complete.")

if __name__ == '__main__':
    main()
