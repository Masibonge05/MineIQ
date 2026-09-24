import pytest
from src.inference.pipeline import analyze

def test_analyze_pipeline():
    res = analyze(None)
    assert "minerals" in res
    assert "processability" in res
    assert "decisions" in res
    assert "latency_ms" in res
    assert "confidence" in res
