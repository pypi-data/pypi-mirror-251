"""
    This module contains functions for extracting relevant 
    information contained in the data obtained through InnerTube 
    (Google's private API for YouTube, YouTube Music, ..)
    The extraction focuses on multimedia contents (songs, videos, 
    podcasts, etc.) and ignores the remaining data (tracking parameters, 
    interface rendering data, etc.)
"""

import logging

from typing import Optional
from typing import Tuple
from typing import List
from typing import Callable
from typing import Dict

from .utils import convert_length
from .utils import convert_number
from .utils import get_item_type

from .endpoints import Endpoint
from .endpoints import BrowseEndpoint
from .endpoints import WatchEndpoint
from .endpoints import UrlEndpoint
from .endpoints import SearchEndpoint

from .containers import CardShelf
from .containers import Shelf
from .containers import ItemsContainer
from .containers import ShelfContainer

from .exceptions import EndpointNotFound
from .exceptions import ITDEBaseException 
from .exceptions import UnregisteredItemType
from .exceptions import KeyNotFound
from .exceptions import UnexpectedState

from .items import Item
from .items import AlbumItem
from .items import VideoItem
from .items import ArtistItem
from .items import PlaylistItem
from .items import SongItem
from .items import SingleItem
from .items import EPItem
from .items import PodcastItem
from .items import ProfileItem
from .items import EpisodeItem

from .ytypes import ShelfStructType
from .ytypes import ResultStrucType
from .ytypes import ShelfItemStructType
from .ytypes import PlaylistItemStructType
from .ytypes import EndpointType
from .ytypes import ShelfType
from .ytypes import ItemType


logger = logging.getLogger(__name__)


def handle(function: Callable) -> Callable:
    """
        Decorator used to collect and handle all possible 
        exceptions that may occur during extraction that 
        are not part of the itde exception family.
        If one of these is launched, something unexpected 
        has happened (most likely the data structures provided 
        by InnerTube have changed)
    """
    def inner_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (
                KeyError,
                IndexError,
                TypeError,
                ValueError,
                ITDEBaseException
        ) as exception:
            logger.critical('An error occured during the data extraction process')
            logger.critical(
                'Please open an issue at '
                'https://github.com/g3nsy/itde/issues '
                'and provide this log output.'
            )
            raise ITDEBaseException(exception)

    return inner_function


@handle
def extract(data: Dict) -> Optional[List]:
    """
        Main method for extracting data provided by InnerTube.

        The idea is to have a single method for data extraction, 
        in order to make the extraction process simpler and more 
        direct.

        The data provided by InnerTube, depending on the type 
        of query provided, can be different in structure, however 
        there are two macro categories of structures:

            - Structures containing shelves (which contain items)

            - Structures containing items

        Structures containing only items are organized into 
        ItemsContainer objects, while structures containing shelves 
        are organized into ShelfContainer objects.
    """

    contents, title = _extract_contents(data)

    # Does this happen if the query is malformed?
    if contents is None:
        return None

    if title:
        container = ItemsContainer(title)
        for entry_item in contents:
            item = _extract_item(entry_item)
            if item:
                container.append(item)
        return container

    # For some reason mypy believes that the 
    # container variable is of type ItemContainer
    container = ShelfContainer()  # type: ignore

    for entry in contents:
        shelf_extraction_result = _extract_shelf(entry)
        if not shelf_extraction_result:
            continue

        shelf, entry_contents = shelf_extraction_result

        item_type = get_item_type(shelf.type)

        for entry_item in entry_contents:
            item = _extract_item(
                entry_item=entry_item,
                item_type=item_type
            )
            if item:
                shelf.append(item)

        container.append(shelf)  # type: ignore

    return container


def _extract_contents(data: Dict) -> Tuple[Optional[List[Dict]], Optional[str]]:
    """
        Extracts the list of main contents. If a title is also present, 
        the list of contents does not contain shelves but items.
        The returned contents list may be None, indicating that the query 
        did not produce any relevant information.
    """
    contents_data = data["contents"]

    if ResultStrucType.SINGLE_COLUMN_BROWSE_RESULTS.value in contents_data:
        tmp = contents_data["singleColumnBrowseResultsRenderer"]["tabs"][0][
            "tabRenderer"]["content"]["sectionListRenderer"]

        if ShelfStructType.GRID.value in tmp["contents"][0]:
            contents = tmp["contents"][0]["gridRenderer"]["items"]
            title = data["header"]["musicHeaderRenderer"]["title"]["runs"][0]["text"]
        else:
            contents = tmp["contents"]
            title = None

    elif ResultStrucType.TABBED_SEARCH_RESULTS.value in contents_data:
        tmp = contents_data["tabbedSearchResultsRenderer"][
            "tabs"][0]["tabRenderer"]["content"]["sectionListRenderer"]
        contents = tmp["contents"]
        title = None

    elif ResultStrucType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in contents_data:
        tmp = contents_data["singleColumnMusicWatchNextResultsRenderer"][
            "tabbedRenderer"]["watchNextTabbedResultsRenderer"]["tabs"][0][
            "tabRenderer"]["content"]["musicQueueRenderer"]

        if "content" not in tmp:  # -> Empty content case
            return None, None

        contents = tmp["content"]["playlistPanelRenderer"]["contents"]
        title = tmp["content"]["playlistPanelRenderer"]["title"]

    else:
        raise KeyNotFound(contents_data.keys())

    return contents, title


def _extract_shelf(entry: Dict) -> Optional[Tuple[Shelf, List[Dict]]]:
    """
        Extracts the shelf from the dictionary provided.
        There are 3 different types of relevant shelves in YouTube Music:

            - Music Shelf
            - Music Card Shelf
            - Music Carousel Shelf

        Each of these has its own particularities and therefore must 
        be managed individually.

        Note: The type of the shelf is used to determine the type of 
        the items contained in them, this is because it is not always 
        possible to determine the type of an item using its data
        Furthermore, the type of a shelf, which is a ShelfType object, 
        describes the shelf name (contained in ShelfType.value)
    """

    if ShelfStructType.MUSIC_SHELF.value in entry:
        key = ShelfStructType.MUSIC_SHELF.value
        shelf_type = ShelfType(entry[key]["title"]["runs"][0]["text"])
        entry_contents = entry[key]["contents"]
        endpoint = _extract_endpoint(data=entry[key]["bottomEndpoint"])
        shelf = Shelf(shelf_type=shelf_type, shelf_endpoint=endpoint)

    elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CAROUSEL_SHELF.value
        shelf_type = ShelfType(
            entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                "title"]["runs"][0]["text"]
        )
        entry_contents = entry[key]["contents"]
        try:
            endpoint = _extract_endpoint(
                data=entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                    "title"]["runs"][0]["navigationEndpoint"]
            )
        except KeyError:
            endpoint = None
        shelf = Shelf(shelf_type=shelf_type, shelf_endpoint=endpoint)

    elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        entry_contents = entry[key].get("contents", [])
        thumbnail_url = entry[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        item_title = entry[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(
            data=entry[key]["title"]["runs"][-1]["navigationEndpoint"]
        )
        shelf = CardShelf(
            name=item_title,
            endpoint=endpoint,
            thumbnail_url=thumbnail_url,
        )

    elif (
            # They are irrelevant
            ShelfStructType.ITEM_SECTION.value in entry
            or ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry
    ):
        return None

    else:
        raise KeyNotFound(entry.keys())

    return shelf, entry_contents


def _extract_item(entry_item: Dict, item_type: Optional[ItemType] = None) -> Optional[Item]:
    """
        Extracts a single item whose type is determined by the item_type 
        parameter if present, otherwise extraction of the item type is attempted.
        The data of an article of the same type may differ depending on the shelf 
        in which it is located. For this reason differences must be managed individually
    """
    if ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
        key = ShelfItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        name = entry_item[key]["flexColumns"][0][
            "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
        if not item_type:
            try:
                item_type = ItemType(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"]["text"]["runs"][0]["text"]
                )
            except ValueError:
                # It appears that 'Song' items 
                # do not have 'Song' in the subtitle
                item_type = ItemType.SONG

        match item_type:

            case ItemType.ARTIST:
                subscribers = convert_number(
                    string=entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["text"]
                )
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = ArtistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )

            case ItemType.ALBUM:
                release_year = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = AlbumItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year),
                )

            case ItemType.VIDEO:
                length = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                views = convert_number(
                    string=entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-3]["text"]
                )
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][-1]["navigationEndpoint"]
                )
                item = VideoItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    views=views,
                )

            case ItemType.PLAYLIST:
                try:
                    length = int(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    length = None
                try:
                    views = convert_number(
                        string=entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    views = None  # type: ignore
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = PlaylistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    views=views,
                )

            case ItemType.SINGLE:
                release_year = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = SingleItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year),
                )

            case ItemType.SONG:
                try:
                    length = convert_length(
                        length=entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except UnexpectedState:
                    length = None
                try:
                    reproduction = convert_number(
                        string=entry_item[key]["flexColumns"][2][
                            "musicResponsiveListItemFlexColumnRenderer"][
                            "text"]["runs"][-1]["text"]
                    )
                except IndexError:
                    reproduction = None
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = SongItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    reproductions=reproduction,
                    artist_items=None,
                    album_item=None,
                )

            case ItemType.EPISODE:
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"][
                        "text"]["runs"][-1]["navigationEndpoint"]
                )
                item = EpisodeItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    publication_date=None,
                    artist_items=None,
                )

            case ItemType.PODCAST:
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = PodcastItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    artist_items=None,
                )

            case ItemType.PROFILE:
                item_handle = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"][
                    "text"]["runs"][-1]["text"]
                item = ProfileItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    handle=item_handle,
                )

            case ItemType.EP:
                endpoint = _extract_endpoint(
                    data=entry_item[key]["navigationEndpoint"]
                )
                item = EPItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url
                )

            case _:
                raise UnregisteredItemType(item_type)

    elif ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
        key = ShelfItemStructType.MUSIC_TWO_ROW_ITEM.value
        thumbnail_url = entry_item[key]["thumbnailRenderer"]["musicThumbnailRenderer"][
            "thumbnail"]["thumbnails"][-1]["url"]
        name = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
        if not item_type:
            try:
                item_type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
            except ValueError:
                item_type = ItemType.SINGLE

        match item_type:

            case ItemType.ARTIST:
                subscribers = convert_number(
                    string=entry_item[key]["subtitle"]["runs"][0]["text"]
                )
                item = ArtistItem(
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )

            case ItemType.ALBUM:
                release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                sub_type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
                match sub_type:
                    case ItemType.ALBUM:
                        item = AlbumItem(  # type: ignore
                            name=name,
                            endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            artist_items=None,
                            release_year=release_year,
                        )

                    case ItemType.EP:
                        item = EPItem(  # type: ignore
                            name=name,
                            endpoint=endpoint,
                            thumbnail_url=thumbnail_url,
                            artist_items=None,
                            release_year=release_year,
                        )
                    case _:
                        raise UnregisteredItemType(sub_type)

            case ItemType.EP:
                release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = EPItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    artist_items=None,
                    release_year=release_year,
                )

            case ItemType.VIDEO:
                views = convert_number(
                    string=entry_item[key]["subtitle"]["runs"][-1]["text"]
                )
                item = VideoItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=views,
                )

            case ItemType.PLAYLIST:
                item = PlaylistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=None,
                )

            case ItemType.SINGLE:
                release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = SingleItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year),
                )

            case ItemType.SONG:
                item = SongItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    reproductions=None,
                    album_item=None,
                )

            case (ItemType.EPISODE | ItemType.PODCAST | ItemType.PROFILE):
                raise UnexpectedState(item_type)

            case _:
                raise UnregisteredItemType(item_type)

    elif PlaylistItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
        key = PlaylistItemStructType.PLAYLIST_PANEL_VIDEO.value
        name = entry_item[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(entry_item[key]["navigationEndpoint"])
        length = convert_length(
            length=entry_item[key]["lengthText"]["runs"][-1]["text"]
        )
        tmp = entry_item[key]["thumbnail"]["thumbnails"][-1]
        thumbnail_url = entry_item[key]["thumbnail"]["thumbnails"][-1]["url"]
        width, height = tmp["width"], tmp["height"]

        # In this case it is impossible to determine the type of the articles
        # It seems that the songs have a cover whose size ratio is 1, 
        # while the remaining items do not
        if width / height == 1:
            item = SongItem(  # type: ignore
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                album_item=None,
                artist_items=None,
            )

        # Podcasts, episodes and videos are collected here.
        else:
            try:
                views = convert_number(
                    string=entry_item[key]["longBylineText"]["runs"][-3]["text"]
                )
            except (KeyError, IndexError):
                views = None

            item = VideoItem(  # type: ignore
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                artist_items=None,
                views=views,
            )

    # These do not contain information of interest for the purposes of this code
    elif (
            PlaylistItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry_item
            or PlaylistItemStructType.PLAYLIST_EXPANDABLE_MESSAGE.value in entry_item
            or ShelfStructType.MESSAGE.value in entry_item
    ):
        return None

    else:
        raise KeyNotFound(f"Content: {entry_item.keys()}")

    return item


def _extract_endpoint(data: Dict) -> Endpoint:
    """
        Constructs and returns an Endpoint object 
        calculated on the specified dictionary.
        If one of the known endpoints is not found, 
        throw an EndpointNotFound exception
    """

    if EndpointType.BROWSE_ENDPOINT.value in data:
        endpoint_data = data["browseEndpoint"]
        browse_id = endpoint_data["browseId"]
        endpoint = BrowseEndpoint(
            browse_id=browse_id,
            params=endpoint_data.get("params", None)
        )

    elif EndpointType.WATCH_ENDPOINT.value in data:
        endpoint_data = data["watchEndpoint"]
        video_id = endpoint_data["videoId"]
        endpoint = WatchEndpoint(  # type: ignore
            video_id=video_id,
            playlist_id=endpoint_data.get("playlist_id", None),
            params=endpoint_data.get("params", None),
        )

    elif EndpointType.SEARCH_ENDPOINT.value in data:
        endpoint_data = data["searchEndpoint"]
        query = endpoint_data["query"]
        endpoint = SearchEndpoint(  # type: ignore
            query=query,
            params=endpoint_data.get("params", None)
        )

    elif EndpointType.URL_ENDPOINT in data:
        endpoint_data = data["urlEndpoint"]
        url = endpoint_data["url"]
        endpoint = UrlEndpoint(  # type: ignore
            url=url,
            params=endpoint_data.get("params", None)
        )

    else:
        raise EndpointNotFound(f"Endpoint not found in: {data}")

    return endpoint
