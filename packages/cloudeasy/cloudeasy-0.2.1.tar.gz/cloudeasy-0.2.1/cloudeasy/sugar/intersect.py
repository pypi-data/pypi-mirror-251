from typing import List, TypeVar, Callable, Tuple, Generic, Iterable

from pydantic import BaseModel

L = TypeVar("L")
R = TypeVar("R")
C = Callable[[L, R], bool]


class Intersection(BaseModel, Generic[L, R]):
    l: List[L]
    r: List[R]
    intersection: List[Tuple[L, R]]

    def __bool__(self):
        return len(self.l) + len(self.r) != 0


def intersect(left: Iterable[L], right: Iterable[R], compare: Callable[[L, R], bool] = lambda x, y: x == y) -> Intersection[L, R]:
    """
    intersection two list,find elements which appear in both list, Which appear only in left and which only in right.
    element in two list may be same or different type.So use check_same to compare if there are logical same.
    It should not be duplicate element within single  left_list nor right_list
    """
    left_only = []
    intersection = []
    for idx, l_ele in enumerate(left):
        found_match = None
        for idy, r_ele in enumerate(right):
            if compare(l_ele, r_ele):
                found_match = (l_ele, r_ele)
        if found_match:
            intersection.append(found_match)
        else:
            left_only.append(l_ele)
    right_only = list(filter(lambda x: x not in [y[1] for y in intersection], right))
    return Intersection[L, R](
        l=left_only,
        r=right_only,
        intersection=intersection
    )
