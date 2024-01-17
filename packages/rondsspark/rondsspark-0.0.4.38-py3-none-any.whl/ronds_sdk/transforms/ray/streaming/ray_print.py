import json
import os

import ray

from ronds_sdk.transforms.ray.base import RayTransform


class RayPrint(RayTransform):

    def __init__(self, parallel=None, worker_index=-1):
        super().__init__(worker_index, parallel=parallel)

    def process(self, inputs):
        print("%s: %s" % (os.getpid(), json.dumps(inputs)))
