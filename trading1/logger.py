import logging, os, sys
from logging.handlers import RotatingFileHandler


cur_dir = os.path.abspath(os.curdir)  # current 의 줄임말. 파이썬이 실행된 경로를 반환하고, 이 경로의 절대경로가 PROJECT_HOME
sys.path.append(cur_dir)
PROJECT_HOME=cur_dir


def get_logger(name):
    """name(str): 생성할 로그 파일명입니다.
    생성될 로그 객체를 반환하는 함수입니다."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    rotate_handler = RotatingFileHandler(PROJECT_HOME+"/logs/"+name+".log", 'a', 1024*1024*5, 5)
    formatter = logging.Formatter('[%(levelname)s]-%(asctime)s-%(filename)s:%(lineno)s:%(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    rotate_handler.setFormatter(formatter)
    logger.addHandler(rotate_handler)
    return logger
