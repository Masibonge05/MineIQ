import pytest
import torch
from src.models.mineral_classifier import MineralClassifier
from src.config import Config

@pytest.fixture
def mock_config():
    return Config(
        project_name="Test",
        version="0.1",
        hidsag_root="",
        incoming_dir="",
        image_size=224,
        batch_size=2,
        seed=42,
        confidence_threshold_high=0.8,
        confidence_threshold_medium=0.6,
        processability_targets=["cu_recovery"],
        rules_file=""
    )

def test_mineral_classifier_build(mock_config):
    clf = MineralClassifier(mock_config)
    model = clf.build()
    assert isinstance(model, torch.nn.Module)
    
def test_mineral_classifier_predict(mock_config):
    clf = MineralClassifier(mock_config)
    res = clf.predict(None)
    assert 'minerals' in res
    assert 'confidence' in res
