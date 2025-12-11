from loguru import logger  # 使用 loguru 进行日志记录
import sys
from pathlib import Path
import json

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.remove()

# Log all levels to stdout
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Log all levels to a file
logger.add(
    "logs/app.log",  # 普通日志文件
    rotation="500 MB",  # 日志文件大小超过500MB时轮转
    retention="10 days",  # 保留10天的日志
    compression="zip",  # 压缩旧的日志文件
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="INFO",
    encoding="utf-8"
)
# Log errors to a separate file
logger.add(
    "logs/error.log",  # 错误日志文件
    rotation="100 MB",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    encoding="utf-8"
)

def get_logger(service: str):
    """获取带有服务名称的 logger"""
    return logger.bind(service=service)

def log_structured(event_type:str,data:dict):
    """记录结构化日志"""
    log_entry = {
        "event_type": event_type,
        "data": data
    }
    logger.info(json.dumps(log_entry, ensure_ascii=False))