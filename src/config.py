import yaml
import os
from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class Config:
    project_name: str
    version: str
    minet_v2_root: str
    hidsag_root: str
    incoming_dir: str
    image_size: int
    batch_size: int
    seed: int
    confidence_threshold_high: float
    confidence_threshold_medium: float
    processability_targets: List[str]
    rules_file: str
    
    @classmethod
    def load(cls, path: str = "configs/config.yaml") -> 'Config':
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at {path}")
            
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)
            
        return cls(
            project_name=raw['project']['name'],
            version=raw['project']['version'],
            minet_v2_root=raw['paths']['minet_v2_root'],
            hidsag_root=raw['paths']['hidsag_root'],
            incoming_dir=raw['paths']['incoming_dir'],
            image_size=raw['data']['image_size'],
            batch_size=raw['data']['batch_size'],
            seed=raw['data']['seed'],
            confidence_threshold_high=raw['mineral_classifier']['confidence_threshold_high'],
            confidence_threshold_medium=raw['mineral_classifier']['confidence_threshold_medium'],
            processability_targets=raw['processability']['targets'],
            rules_file=raw['decision']['rules_file']
        )
