from typing import TypedDict, List


class PaginationSearch(TypedDict):
    field: str
    value: str


class PaginationSort(TypedDict):
    field: str
    by: str


class Pagination(TypedDict):
    skip: int
    take: int
    sort: List[PaginationSort]
    search: List[PaginationSearch]
