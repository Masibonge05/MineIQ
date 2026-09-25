import os
import json
import logging
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.models.processability import ProcessabilityModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockConfig:
    processability_targets = ["cu_recovery", "mo_recovery", "bwi", "lime_consumption", "ph"]

def main():
    logger.info("Starting Processability Training...")
    config = MockConfig()
    
    # 1. Load Data (Mocking HIDSAG GEOMET data load as per README)
    # HIDSAG GEOMET has 146 samples. We simulate the feature extraction here.
    logger.info("Loading HIDSAG GEOMET data (Simulated)...")
    np.random.seed(42)
    n_samples = 146
    
    # Simulate features: Quartz, Pyrite, Chalcopyrite, K-Feldspar, Alunite, Silica, Grain_Size
    X = np.random.rand(n_samples, 7) * 100 
    
    # Simulate target variables
    y_dict = {
        "cu_recovery": 70 + 20 * np.random.rand(n_samples), # 70-90%
        "mo_recovery": 50 + 30 * np.random.rand(n_samples), # 50-80%
        "bwi": 10 + 10 * np.random.rand(n_samples),         # 10-20 kWh/t
        "lime_consumption": 1 + 2 * np.random.rand(n_samples),
        "ph": 6 + 4 * np.random.rand(n_samples)
    }
    
    # Split data (70/30)
    X_train, X_test = train_test_split(X, test_size=0.3, random_state=42)
    y_train_dict = {}
    y_test_dict = {}
    for target in config.processability_targets:
        y_train_dict[target], y_test_dict[target] = train_test_split(y_dict[target], test_size=0.3, random_state=42)
    
    # 2. Build and Train Model
    model = ProcessabilityModel(config)
    model.build()
    model.train(X_train, y_train_dict)
    
    # 3. Evaluate Model
    logger.info("Evaluating model on test set...")
    metrics = {}
    for target in config.processability_targets:
        y_true = y_test_dict[target]
        # Predict uses the "mid" model internally for the value
        preds = [model.predict(x) for x in X_test]
        y_pred = [p[target]["value"] for p in preds]
        y_low = [p[target]["low"] for p in preds]
        y_high = [p[target]["high"] for p in preds]
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        
        # Calculate coverage of 90% prediction interval
        coverage = np.mean([1 if low <= true <= high else 0 for low, high, true in zip(y_low, y_high, y_true)])
        
        metrics[target] = {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "PI_Coverage": float(coverage)
        }
        logger.info(f"{target.upper()} -> MAE: {mae:.2f}, RMSE: {rmse:.2f}, 90% PI Coverage: {coverage:.1%}")
        
    # 4. Save Artifacts
    os.makedirs("outputs/checkpoints", exist_ok=True)
    os.makedirs("outputs/metrics", exist_ok=True)
    
    model_path = "outputs/checkpoints/processability_model.pkl"
    model.save(model_path)
    
    metrics_path = "outputs/metrics/processability_metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)
    logger.info(f"Metrics successfully saved to {metrics_path}")
    logger.info("Training complete.")

if __name__ == '__main__':
    main()
