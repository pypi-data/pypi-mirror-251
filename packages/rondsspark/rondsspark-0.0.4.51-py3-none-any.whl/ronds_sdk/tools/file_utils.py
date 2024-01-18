import importlib.machinery
import os
import sys
import tarfile
import traceback
import zipfile
from functools import lru_cache
from typing import Callable

import ujson
from retrying import retry

from ronds_sdk import error, logger_config

logger = logger_config.config()


class FileUtils(object):

    SYS_PATH_SET = set()

    @staticmethod
    def load_json(file_path):
        # type: (str) -> dict
        with open(file_path, 'r', encoding='utf-8') as f:
            return ujson.load(f)

    @staticmethod
    @lru_cache(maxsize=100)
    def is_compressed_file(file_name):
        file_extension = os.path.splitext(file_name)[1]
        return file_extension in ['.zip', '.tar', '.gz', '.bz2', '.xz']

    @staticmethod
    @retry(stop_max_attempt_number=3, stop_max_delay=60000)
    @lru_cache(maxsize=100)
    def load_module_func(alg_absolute_path, func_name):
        logger.info("alg_absolute_path: %s, func_name: %s" % (alg_absolute_path, func_name))
        if FileUtils.is_compressed_file(alg_absolute_path):
            return FileUtils.load_module_func_zip(alg_absolute_path, func_name)
        return FileUtils.load_module_func_dir(alg_absolute_path, func_name)

    @staticmethod
    def load_module_func_zip(alg_absolute_path, func_name):
        alg_absolute_path = FileUtils.uncompress_file(alg_absolute_path)
        return FileUtils.load_module_func_dir(alg_absolute_path, func_name)

    @staticmethod
    def load_module_func_dir(alg_absolute_path, func_name):
        # type: (str, str) -> Callable[..., str]
        if alg_absolute_path not in sys.path:
            sys.path.append(alg_absolute_path)

        func_path_array = func_name.split('.')
        if len(func_path_array) <= 1:
            raise error.TransformError("""algorithm func path expect the format: file.function_name, 
                                                  but found: %s""" % func_name)
        model_name = '.'.join(func_path_array[0:-1])
        model_path = '%s/%s.py' % (alg_absolute_path, model_name)
        func = func_path_array[-1]

        alg_model = importlib.machinery.SourceFileLoader(model_name, model_path).load_module()
        alg_func = getattr(alg_model, func)
        if alg_func is None:
            raise error.TransformError("""failed load algorithm """)
        return alg_func

    @staticmethod
    def uncompress_file(zip_path, extract_path=None):
        if extract_path is None:
            file_path = os.path.split(os.path.splitext(zip_path)[0])
            extract_path = '%s/tmp/%s_%s' % (file_path[0], file_path[1], os.getpid())
        logger.info('zip_path: %s, extract_path: %s' % (zip_path, extract_path))
        file_extension = os.path.splitext(zip_path)[1]
        if '.gz' == file_extension:
            FileUtils.un_tar_file(zip_path, extract_path)
        elif '.zip' == file_extension:
            FileUtils.unzip_file(zip_path, extract_path)
        else:
            raise error.RondsError('unsupported compression type: %s' % file_extension)
        return extract_path

    @staticmethod
    def unzip_file(zip_path, extract_path):
        logger.info('unzip_file, zip_path: %s, extract_path: %s' % (zip_path, extract_path))
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            try:
                for member in zip_ref.infolist():
                    file_path = os.path.join(extract_path, member.filename)
                    if not os.path.exists(file_path):
                        zip_ref.extract(member, extract_path)
            except FileExistsError as ex:
                logger.warning("file exited: %s, %s, %s" % (extract_path, ex, traceback.format_exc()))

    @staticmethod
    def un_tar_file(tar_path, extract_path):
        logger.info('un_tar_file, tar_path: %s, extract_path: %s' % (tar_path, extract_path))
        try:
            with tarfile.open(tar_path, 'r:gz') as tar_ref:
                for member in tar_ref.getmembers():
                    file_path = os.path.join(extract_path, member.path)
                    if not os.path.exists(file_path):
                        tar_ref.extract(member, extract_path)
        except FileExistsError as ex:
            logger.warning("file exited: %s, %s, %s" % (extract_path, ex, traceback.format_exc()))
