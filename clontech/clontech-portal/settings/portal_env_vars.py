import os

dir_up = os.path.dirname

BASE_DIR = dir_up(dir_up(os.path.abspath(__file__)))
os.environ.setdefault('BASE_DIR', BASE_DIR)
os.environ.setdefault('BASE_ROOT', BASE_DIR)
