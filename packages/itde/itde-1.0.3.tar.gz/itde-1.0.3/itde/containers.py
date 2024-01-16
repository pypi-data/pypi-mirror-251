from typing import Optional
from .items import Item
from .ytypes import ShelfType
from .endpoints import Endpoint


class ShelfContainer(list):
    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return (
            'ShelfContainer{'
            f'shelves={super().__repr__()}'
            '}'
        )


class Shelf(list):
    def __init__(
            self,
            shelf_type: ShelfType,
            shelf_endpoint: Optional[Endpoint] = None
    ) -> None:
        super().__init__()
        self.type = shelf_type
        self.endpoint = shelf_endpoint

    def __repr__(self) -> str:
        return (
            'Shelf{'
            f'type={self.type}, '
            f'endpoint={self.endpoint}, '
            f'items={super().__repr__()}'
            '}'
        )


class CardShelf(Item, Shelf):
    def __init__(
            self,
            name: str,
            endpoint: Endpoint,
            thumbnail_url: str
    ) -> None:
        super().__init__(
            name=name,
            endpoint=endpoint,
            thumbnail_url=thumbnail_url,
        )

        self.endpoint = None
        self.type = ShelfType.TOP_RESULT

    def __repr__(self) -> str:
        return (
            'CardShelf{'
            f'name={self.name}, '
            f'endpoint={self.endpoint}, '
            f'thumbnail_url={self.thumbnail_url}, '
            f'{super(Item, self).__repr__()}'
            '}'
        )


class ItemsContainer(list):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return (
            'Container{'
            f'name={self.name}, '
            f'items={super().__repr__()}'
            '}'
        )
