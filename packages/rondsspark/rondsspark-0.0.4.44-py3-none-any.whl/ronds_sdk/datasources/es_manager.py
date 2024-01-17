from elasticsearch import Elasticsearch

from ronds_sdk import logger_config
from ronds_sdk.options.pipeline_options import ESOptions
from ronds_sdk.tools.metaclass import Singleton

logger = logger_config.config()


class ESManager(metaclass=Singleton):
    def __init__(self, options: 'ESOptions'):
        self.port = options.port
        self.nodes = options.nodes
        self.index_auto_create = options.index_auto_create
        self.index = options.index
        end_points = ['http://' + node + ':' + str(self.port) for node in self.nodes]
        self.client = Elasticsearch(end_points)

    # 添加记录
    async def add_data(self,
                 index_name,  # type: str
                 data  # type: dict
                 ):
        try:
            response = self.client.index(index=index_name, body=data)
            return response
        except Exception as err:
            logger.error(err)
        return None

    # 新增索引
    def create_index(self,
                     index_name,  # type: str
                     mapping  # type: dict
                     ):
        try:
            # 检查索引是否存在
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(index=index_name, body=mapping)
                return True
            else:
                logger.info(f"索引 {index_name} 已经存在")
            return False
        except Exception as err:
            logger.error(err)
        return False
