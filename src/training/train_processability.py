import logging
from src.config import Config
from src.models.processability import ProcessabilityModel

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Processability Training...")
    config = Config.load()
    model = ProcessabilityModel(config)
    model.build()
    
    # TODO(person-3): Implement XGBoost training loop
    logger.info("Training complete.")

if __name__ == '__main__':
    main()
