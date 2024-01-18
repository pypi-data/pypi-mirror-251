import ujson

from ronds_sdk.transforms.ray.base import RayTransform


class RayPrint(RayTransform):

    def __init__(self, parallel=None, worker_index=-1):
        super().__init__(worker_index, parallel=parallel)

    async def consume(self):
        # from ronds_sdk.tools import utils
        # utils.break_point()
        await super().consume()

    async def process(self, inputs):
        for p_name, record in inputs.items():
            print("%s: \n%s\n" % (p_name, ujson.dumps(record)))
            yield record
