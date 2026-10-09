import logging
from config.settings import LOGS_DIR

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.WARNING)
    
    # File handler — logs file lo save avutai
    log_file = LOGS_DIR / f"{name}.log"
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.WARNING)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # Console handler — REMOVED (no logs in console)
    
    return logger
