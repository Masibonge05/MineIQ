import logging
import yaml
import os

def setup_logging(config_path: str = "configs/config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    log_config = config.get("logging", {})
    level_str = log_config.get("level", "INFO")
    fmt = log_config.get("format", "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    
    level = getattr(logging, level_str.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format=fmt,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(config['paths']['logs'], "mineiq.log"), mode='a')
        ]
    )
    
    return logging.getLogger("MineIQ")
