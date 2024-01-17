from enum import Enum

# 工艺数据类型
PROCESS_DATA_TYPE = 106

# 特征值数据类型
INDEX_DATA_TYPE = 101

DEFAULT_RETRY = 3


# noinspection SpellCheckingInspection
class JsonKey(Enum):
    NAMES = 'names'
    DEVICE_ID = 'deviceid'


class Constant(Enum):
    NAN = 'nan'
