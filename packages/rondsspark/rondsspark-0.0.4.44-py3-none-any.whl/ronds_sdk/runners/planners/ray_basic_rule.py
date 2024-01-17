from typing import TYPE_CHECKING

from ronds_sdk.runners.planners import BFSPipeRule

if TYPE_CHECKING:
    from ronds_sdk import Pipeline
    from ronds_sdk.transforms.ptransform import PTransform


__all__ = [
    'BasicParamRule'
]


class BasicParamRule(BFSPipeRule):
    """
    check and make up basic params for RayTransform, e.g. pipeline
    """

    def on_match(self, transform: 'PTransform', pipeline: 'Pipeline') -> 'PTransform':
        if transform.pipeline is None:
            transform.pipeline = pipeline
        return transform
