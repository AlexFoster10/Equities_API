import logging

def get_logger():
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler("app/testing/mainlog.log", mode="w")      
    handler.setFormatter(formatter)
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger