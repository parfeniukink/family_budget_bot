from typing import Iterable

from categories.domain import CategoriesError, CategoriesMapping, Category
from db import database
from shared.sequences import build_dict_from_sequence


class CategoriesCache(type):
    __TABLE = "categories"

    @classmethod
    def __fetch_categories(cls) -> list[Category]:
        data = [Category(**item) for item in database.fetchall(cls.__TABLE)]
        return data

    def __getattr__(cls, attr):
        if attr == "CACHED_CATEGORIES":
            data = cls.__fetch_categories()
            setattr(cls, attr, data)
            return data
        raise AttributeError(attr)


class CategoriesService(metaclass=CategoriesCache):
    CACHED_CATEGORIES: list[Category]

    @classmethod
    def get_by_name(cls, name: str) -> Category:
        for category in cls.CACHED_CATEGORIES:
            if category.name == name:
                return category
        raise CategoriesError()

    @classmethod
    def get_by_id(cls, id: int) -> Category | None:
        for category in cls.CACHED_CATEGORIES:
            if category.id == id:
                return category
        return None

    @classmethod
    def get_ordered(cls) -> Iterable[Category]:
        """Returns cached categories in CategoriesMapping order"""

        categories_by_name: dict[str, Category] = build_dict_from_sequence(
            cls.CACHED_CATEGORIES,
            key="name",
        )  # type: ignore
        return [categories_by_name[name] for name in CategoriesMapping.values()]
