from ronds_sdk.options.pipeline_options import MinioOptions
from minio import Minio
from minio.credentials import StaticProvider
from minio.error import MinioException, InvalidResponseError

from ronds_sdk.tools.metaclass import Singleton


class MinioManager(metaclass=Singleton):
    def __init__(self, options: 'MinioOptions'):
        self.port = options.port
        self.address = options.address
        self.username = options.username
        self.password = options.password
        self.buckets = options.buckets
        self.bucket_name = self.buckets[0]
        self.endpoint = self.address + ":" + str(self.port)
        self.file_path = "/rayWorkflow"
        # 创建MinIO客户端，并使用Identity Provider进行身份验证
        self.client = Minio(self.endpoint,
                            credentials=StaticProvider(
                                self.username, self.password))

    def create_bucket(self, bucket_name):
        if self.client.bucket_exists(bucket_name):
            print(f'Bucket {bucket_name} already exists.')
            return True
        try:
            # 创建存储桶
            self.client.make_bucket(bucket_name)
            return True
        except MinioException as err:
            print(err)
        return False

    def upload_file(self, object_name):
        try:
            # 上传文件
            self.client.fput_object(self.bucket_name, object_name, self.file_path)
            return True
        except InvalidResponseError as err:
            print(err)
        return False

    def download_file(self, object_name):
        try:
            # 下载文件
            self.client.fget_object(self.bucket_name, object_name, self.file_path)
            return True
        except InvalidResponseError as err:
            print(err)
        return False

    def delete_file(self, object_name):
        try:
            # 删除文件
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except InvalidResponseError as err:
            print(err)
        return False

    def delete_bucket(self, bucket_name):
        try:
            # 删除存储桶
            self.client.remove_bucket(bucket_name)
            return True
        except InvalidResponseError as err:
            print(err)
        return False
