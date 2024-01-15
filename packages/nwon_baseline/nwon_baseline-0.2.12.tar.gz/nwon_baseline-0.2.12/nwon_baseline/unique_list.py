from typing import Iterable, Union


def unique_list(
    list_to_check: Union[
        Iterable[Union[str, int, float, bool, bytes]],
        Iterable[str],
        Iterable[int],
        Iterable[float],
        Iterable[bool],
        Iterable[bytes],
    ]
):
    """
    Unifies items in a list.
    """

    seen = set()
    seen_add = seen.add
    return [x for x in list_to_check if not (x in seen or seen_add(x))]
