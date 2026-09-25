import time
import logging
import numpy as np
from src.models.mineral_classifier import MineralClassifier
from src.models.processability import ProcessabilityModel
from src.decision.engine import DecisionEngine
from src.config import Config

logger = logging.getLogger(__name__)

# Cache models globally for Streamlit so we don't reload on every frame
_classifier = None
_process_model = None
_engine = None

def get_models(config):
    global _classifier, _process_model, _engine
    if _engine is None:
        _classifier = MineralClassifier(config)
        # _classifier.load(...)  # To be implemented by Person 2
        
        _process_model = ProcessabilityModel(config)
        try:
            _process_model.load("outputs/checkpoints/processability_model.pkl")
        except Exception as e:
            logger.warning(f"Could not load processability model: {e}")
            
        _engine = DecisionEngine('configs/rules.yaml')
    return _classifier, _process_model, _engine

def analyze(image_path_or_array) -> dict:
    start_time = time.time()
    config = Config.load()
    classifier, process_model, engine = get_models(config)
    
    logger.info("Running Mineral Classifier...")
    class_res = classifier.predict(image_path_or_array)
    
    logger.info("Running Processability Model...")
    # Convert classifier output to the 7 features expected by ProcessabilityModel
    minerals = class_res['minerals']
    
    # Scale from 0-1 to 0-100 since the training script used 0-100
    # Fallback to simulated defaults if classifier (Person 2) doesn't output these yet
    features = np.array([
        minerals.get('quartz', 0.1) * 100,
        minerals.get('pyrite', 0.2) * 100,
        minerals.get('chalcopyrite', 0.4) * 100,
        minerals.get('k-feldspar', 0.15) * 100,
        minerals.get('alunite', 0.05) * 100,
        minerals.get('silica', 0.1) * 100,
        50.0 # Mock grain size
    ]).reshape(1, -1)
    
    proc_res = process_model.predict(features)
    
    logger.info("Evaluating Decision Engine...")
    # Engine expects minerals in 0-100 format if rules are > 1
    engine_minerals = {k: v*100 for k, v in minerals.items()}
    engine_minerals['k-feldspar'] = features[0][3]
    engine_minerals['alunite'] = features[0][4]
    engine_minerals['silica'] = features[0][5]
    
    decisions = engine.evaluate(engine_minerals, proc_res, class_res['confidence'])
    
    latency_ms = int((time.time() - start_time) * 1000)
    
    confidence_level = "LOW"
    if class_res['confidence'] > 0.8:
        confidence_level = "HIGH"
    elif class_res['confidence'] >= 0.6:
        confidence_level = "MEDIUM"
        
    return {
        "minerals": class_res['minerals'],
        "processability": proc_res,
        "decisions": decisions,
        "latency_ms": latency_ms,
        "confidence": confidence_level,
        "confidence_score": class_res['confidence']
    }
