from categories.domain import CategoriesError, Category
from db import database


class CategoriesCache(type):
    __TABLE = "categories"

    @classmethod
    def get_categories(cls) -> list[Category]:
        data = [Category(**item) for item in database.fetchall(cls.__TABLE)]
        return data

    def __getattr__(cls, attr):
        if attr == "CACHED_CATEGORIES":
            data = cls.get_categories()
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
