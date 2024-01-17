from typing import Optional
from .ytypes import EndpointType


class Endpoint:
    def __init__(
            self,
            params: Optional[str] = None
    ) -> None:
        self.params = params
        self.type: Optional[EndpointType] = None

    def __repr__(self):
        return (
            "Endpoint{"
            f"type={self.type}, "
            f"params={self.params}"
            "}"
        )


class BrowseEndpoint(Endpoint):
    def __init__(
            self,
            browse_id: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.browse_id: str = browse_id
        self.type = EndpointType.BROWSE_ENDPOINT

    def __repr__(self):
        return (
                super().__repr__()[:-1] +
                f", browse_id={self.browse_id}" 
                "}"
        )


class SearchEndpoint(Endpoint):
    def __init__(
            self,
            query: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.query: str = query
        self.type = EndpointType.SEARCH_ENDPOINT

    def __repr__(self):
        return (
                super().__repr__()[:-1] +
                f", query={self.query}" 
                "}"
        )


class WatchEndpoint(Endpoint):
    def __init__(
            self,
            video_id: str,
            playlist_id: Optional[str] = None,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.video_id = video_id
        self.playlist_id = playlist_id
        self.type = EndpointType.WATCH_ENDPOINT

    def __repr__(self):
        return (
                super().__repr__()[:-1] +
                f", video_id={self.video_id}"
                f", playlist_id={self.playlist_id}"
                "}"
        )


class UrlEndpoint(Endpoint):
    def __init__(
            self,
            url: str,
            *args,
            **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.url: str = url
        self.type = EndpointType.URL_ENDPOINT

    def __repr__(self):
        return (
                super().__repr__()[:-1] +
                f", url={self.url}" 
                "}"
        )
