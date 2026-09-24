import time
import logging
from src.models.mineral_classifier import MineralClassifier
from src.models.processability import ProcessabilityModel
from src.decision.engine import DecisionEngine
from src.config import Config

logger = logging.getLogger(__name__)

def analyze(image_path_or_array) -> dict:
    start_time = time.time()
    
    # Load config and initialize components (in production, initialize once and keep in memory)
    config = Config.load()
    classifier = MineralClassifier(config)
    process_model = ProcessabilityModel(config)
    engine = DecisionEngine(config.rules_file)
    
    logger.info("Running Mineral Classifier...")
    class_res = classifier.predict(image_path_or_array)
    
    logger.info("Running Processability Model...")
    proc_res = process_model.predict(image_path_or_array)
    
    logger.info("Evaluating Decision Engine...")
    decisions = engine.evaluate(class_res['minerals'], proc_res, class_res['confidence'])
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    confidence_level = "LOW"
    if class_res['confidence'] >= config.confidence_threshold_high:
        confidence_level = "HIGH"
    elif class_res['confidence'] >= config.confidence_threshold_medium:
        confidence_level = "MEDIUM"
        
    return {
        "minerals": class_res['minerals'],
        "processability": proc_res,
        "decisions": decisions,
        "latency_ms": latency_ms,
        "confidence": confidence_level,
        "confidence_score": class_res['confidence']
    }
