from datetime import date
from datetime import time
from typing import List
from typing import Optional
from .endpoints import Endpoint
from .ytypes import ItemType


class Item:
    def __init__(
            self,
            name: str,
            endpoint: Endpoint,
            thumbnail_url: str
     ) -> None:

        self.name = name
        self.endpoint = endpoint
        self.thumbnail_url = thumbnail_url
        self.type = None

    def __repr__(self) -> str:
        return (
            'Item{'
            f'type={self.type}, '
            f'name={self.name}, '
            f'endpoint={self.endpoint}, '
            f'thumbnail_url={self.thumbnail_url}'
            '}'
        )


class ArtistItem(Item):
    def __init__(
            self,
            subscribers: Optional[int] = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.subscribers = subscribers
        self.type = ItemType.ARTIST

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', subscribers={self.subscribers}'
            '}'
        )


class ItemWithArtist(Item):
    def __init__(
            self,
            artist_items: Optional[List[ArtistItem]] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.artist_items = artist_items
        self.type = None

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', artist_items={self.artist_items}'
            '}'
        )


class VideoItem(ItemWithArtist):
    def __init__(
            self,
            length: Optional[time] = None,
            views: Optional[int] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.length = length
        self.views = views
        self.type = ItemType.VIDEO

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', length={self.length}'
            f', views={self.views}'
            '}'
        )


class AlbumItem(ItemWithArtist):
    def __init__(
            self,
            release_year: Optional[int] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.release_year = release_year
        self.type = ItemType.ALBUM

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', release_year={self.release_year}'
            '}'
        )


class EPItem(AlbumItem):
    def __init__(
            self,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.type = ItemType.EP


class PlaylistItem(ItemWithArtist):
    def __init__(
            self,
            length: Optional[int] = None,
            views: Optional[int] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.length = length
        self.views = views
        self.type = ItemType.PLAYLIST

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', length={self.length}'
            f', views={self.views}'
            '}'
        )


class SingleItem(ItemWithArtist):
    def __init__(
            self,
            release_year: Optional[int] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.release_year = release_year
        self.type = ItemType.SINGLE

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', release_year={self.release_year}'
            '}'
        )


class SongItem(ItemWithArtist):
    def __init__(
            self,
            length: Optional[time] = None,
            reproductions: Optional[int] = None,
            album_item: Optional[AlbumItem] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.length = length
        self.reproductions = reproductions
        self.album_item = album_item
        self.type = ItemType.SONG

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', length={self.length}'
            f', reproductions={self.reproductions}'
            f', album_item={self.album_item}'
            '}'
        )


class ProfileItem(Item):
    def __init__(
            self,
            handle: Optional[str] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.handle = handle
        self.type = ItemType.PROFILE

    def __repr__(self) -> str:
        return (
            super().__repr__()[:-1] +
            f', handle={self.handle}'
            '}'
        )


class PodcastItem(ItemWithArtist):
    def __init__(
            self,
            length: Optional[time] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.length = length
        self.type = ItemType.PODCAST

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', length={self.length}'
            '}'
        )


class EpisodeItem(ItemWithArtist):
    def __init__(
            self,
            publication_date: Optional[date] = None,
            length: Optional[time] = None,
            *args,
            **kwargs
    ) -> None:

        super().__init__(*args, **kwargs)
        self.length = length
        self.publication_date = publication_date
        self.type = ItemType.PODCAST

    def __repr__(self):
        return (
            super().__repr__()[:-1] +
            f', publication_date={self.publication_date}'
            f', length={self.length}'
            '}'
        )
