import logging
from pathlib import Path
from config.settings import LOGS_DIR

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.WARNING)          # ← INFO → WARNING
    
    # File handler
    log_file = LOGS_DIR / f"{name}.log"
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.WARNING)              # ← INFO → WARNING
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)              # ← INFO → WARNING
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger
