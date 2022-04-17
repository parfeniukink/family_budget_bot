from operator import getitem
from typing import Hashable, Sequence, TypeVar

from shared.collections import Model

_Member = TypeVar("_Member", dict, Model)


def build_dict_from_sequence(seq: Sequence[_Member], key: str) -> dict[Hashable, _Member]:
    """
    Build dict from sequence like list to have O(1) complexity for finding values by a specific key.
    Index is used to compare elements with same ID.
    """

    if not seq or not isinstance(seq, Sequence):
        return {}

    if isinstance(seq[0], dict):
        return {getitem(item, key): item for item in seq}  # type: ignore
        # If you need to resolve key duplicates use index
        # return {d[key]: dict(**d, index=index) for (index, d) in enumerate(seq)}

    if isinstance(seq[0], Model):
        return {getattr(element, key): element for element in seq}

    raise ValueError("Unsupported type for build operation")
