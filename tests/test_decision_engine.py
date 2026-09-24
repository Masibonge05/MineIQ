import pytest
from src.decision.engine import DecisionEngine

def test_decision_engine_evaluate():
    # Use the yaml we generated in config
    engine = DecisionEngine("configs/rules.yaml")
    
    minerals = {"pyrite": 0.25}
    predictions = {"cu_recovery": {"value": 65.0}}
    confidence = 0.85
    
    decisions = engine.evaluate(minerals, predictions, confidence)
    
    # Should trigger low_recovery_high_confidence and high_pyrite
    assert len(decisions) >= 2
    priorities = [d['priority'] for d in decisions]
    assert 'HIGH' in priorities
