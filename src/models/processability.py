import joblib
import os
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

class ProcessabilityModel:
    def __init__(self, config=None):
        self.config = config
        self.targets = ["cu_recovery", "mo_recovery", "bwi", "lime_consumption", "ph"]
        if config and hasattr(config, 'processability_targets'):
            self.targets = config.processability_targets
        self.models = {}
        
    def build(self):
        # We use GradientBoostingRegressor for its native support of quantile loss
        # We train three models per target: 5th percentile, median, and 95th percentile
        for target in self.targets:
            self.models[target] = {
                "low": GradientBoostingRegressor(loss='quantile', alpha=0.05, n_estimators=100, max_depth=3, random_state=42),
                "mid": GradientBoostingRegressor(loss='quantile', alpha=0.50, n_estimators=100, max_depth=3, random_state=42),
                "high": GradientBoostingRegressor(loss='quantile', alpha=0.95, n_estimators=100, max_depth=3, random_state=42)
            }
            
    def train(self, X, y_dict):
        """
        Trains the quantile models.
        X: feature matrix
        y_dict: dictionary mapping target names to target arrays
        """
        for target in self.targets:
            if target in y_dict:
                y = y_dict[target]
                # Drop NaNs if any exist in the data
                mask = ~np.isnan(y)
                X_clean, y_clean = X[mask], y[mask]
                
                print(f"Training quantile regressors for {target}...")
                self.models[target]["low"].fit(X_clean, y_clean)
                self.models[target]["mid"].fit(X_clean, y_clean)
                self.models[target]["high"].fit(X_clean, y_clean)
        
    def predict(self, X) -> dict:
        """
        Returns predictions with 90% uncertainty intervals.
        """
        # Check if models are built and trained
        if not self.models or self.targets[0] not in self.models or not hasattr(self.models[self.targets[0]]["mid"], 'estimators_'):
            # Fallback mock for dashboard baseline before training is completed
            return {
                "cu_recovery": {"value": 82.1, "low": 78.4, "high": 85.6},
                "mo_recovery": {"value": 60.5, "low": 55.0, "high": 65.0},
                "bwi": {"value": 15.2, "low": 14.1, "high": 16.3},
                "lime_consumption": {"value": 1.5, "low": 1.2, "high": 1.8},
                "ph": {"value": 7.5, "low": 6.8, "high": 8.1}
            }
            
        # Guarantee X is 2D
        if len(np.shape(X)) == 1:
            X = [X]
            
        results = {}
        for target in self.targets:
            if target in self.models and hasattr(self.models[target]["mid"], 'estimators_'):
                val = self.models[target]["mid"].predict(X)[0]
                low = self.models[target]["low"].predict(X)[0]
                high = self.models[target]["high"].predict(X)[0]
                results[target] = {
                    "value": float(val),
                    "low": float(low),
                    "high": float(high)
                }
        return results
        
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.models, path)
        print(f"Processability models saved to {path}")
        
    def load(self, path):
        self.models = joblib.load(path)
        print(f"Processability models loaded from {path}")
