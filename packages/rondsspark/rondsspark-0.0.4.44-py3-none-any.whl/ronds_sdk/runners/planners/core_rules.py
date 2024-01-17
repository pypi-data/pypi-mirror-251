from ronds_sdk.runners.planners.parallel_rule import *
from ronds_sdk.runners.planners.ray_basic_rule import BasicParamRule
from ronds_sdk.runners.planners.ray_remote_rule import *


class CoreRules(object):

    RAY_BASIC_PARAM_RULE = BasicParamRule()

    # Graph logical node expand to parallel worker nodes
    RAY_STREAM_CONVERT_RULE = RayStreamConvertRule()

    RAY_PLACEMENT_GROUP_RULE = RayPlacementGroupRule()

    # Graph logical node expand to physical node
    RAY_STREAM_PHYSICAL_RULE = RayStreamPhysicalRule()

    # set transform parallel
    RAY_PARALLEL_RULE = ParallelRule()

    # merge 1:1 transforms to a stage transform
    RAY_MERGE_SINGLE_RULE = MergeSingleRule()
