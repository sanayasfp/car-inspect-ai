from libs.env import env

# Access the variables
TMP_DIR = env.get_or_fail("TMP_DIR")
ML_DIR = env.get_or_fail("ML_DIR")
MODELS_DIR = env.get_or_fail("MODELS_DIR")
CAR_PARTS_SEGMENTATION_DIR = env.get_or_fail("CAR_PARTS_SEGMENTATION_DIR")
CAR_PARTS_SEGMENTATION_GIT_URL = env.get_or_fail("CAR_PARTS_SEGMENTATION_GIT_URL")
DB_DIR = env.get_or_fail("DB_DIR")
DB_NAME = env.get_or_fail("DB_NAME")
TRAIN_LOG_TABLE = env.get_or_fail("TRAIN_LOG_TABLE")
LANG = env.get_or_fail("LANG")
