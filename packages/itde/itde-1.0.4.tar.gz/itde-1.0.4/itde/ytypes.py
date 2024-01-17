from enum import Enum


class ResultStrucType(Enum):
    """
        Different structures for accessing the information of interest. 
        From these we arrive at the structures containing the items.
    """
    TABBED_SEARCH_RESULTS = "tabbedSearchResultsRenderer"
    SINGLE_COLUMN_BROWSE_RESULTS = "singleColumnBrowseResultsRenderer"
    SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT = "singleColumnMusicWatchNextResultsRenderer"


class PanelStructType(Enum):
    """
        This structure is equivalent to the shelves with the difference 
        that within the data it is unique and contains all the information 
        of interest. It is found in the data obtained when querying for playlist_id.
    """
    PLAYLIST_PANEL = "playlistPanelRenderer"


class ShelfStructType(Enum):
    """
        Different types of shelf structures found within the main content.
        Some of these structures are ignored during extraction because
        they contain information that is irrelevant for the purposes of this code.

        Structures ignored:
            -> MESSAGE
            -> MUSIC_DESCRIPTION_SHELF
            -> ITEM_SECTION

        Structures not ignored:
            -> GRID
            -> MUSIC_SHELF
            -> MUSIC_CARD_SHELF
            -> MUSIC_CAROUSEL_SHELF
    """
    GRID = "gridRenderer"
    MESSAGE = "messageRenderer"
    MUSIC_SHELF = "musicShelfRenderer"
    MUSIC_CARD_SHELF = "musicCardShelfRenderer"
    MUSIC_CAROUSEL_SHELF = "musicCarouselShelfRenderer"
    MUSIC_DESCRIPTION_SHELF = "musicDescriptionShelfRenderer"
    ITEM_SECTION = "itemSectionRenderer"


class PlaylistItemStructType(Enum):
    """
        Different types of item structures found within playlists
    """
    PLAYLIST_PANEL_VIDEO = "playlistPanelVideoRenderer"
    PLAYLIST_EXPANDABLE_MESSAGE = "playlistExpandableMessageRenderer"
    AUTOMIX_PREVIEW_VIDEO = "automixPreviewVideoRenderer"


class ShelfItemStructType(Enum):
    """
        Different types of item structures found inside the shelves.
    """
    MUSIC_TWO_ROW_ITEM = "musicTwoRowItemRenderer"
    MUSIC_RESPONSIVE_LIST_ITEM = "musicResponsiveListItemRenderer"


class ShelfType(Enum):
    """ 
        Different types of shelves in YouTube Music
    """
    TOP_RESULT = "Top result"
    SONG = "Song"
    VIDEO = "Video"
    PLAYLIST = "Playlist"
    ALBUM = "Album"
    ARTIST = "Artist"
    EPISODE = "Episode"
    SONGS = "Songs"
    VIDEOS = "Videos"
    COMMUNITY_PLAYLIST = "Community playlists"
    FEATURED_PLAYLIST = "Featured playlists"
    ALBUMS = "Albums"
    ARTISTS = "Artists"
    SINGLES = "Singles"
    EPISODES = "Episodes"
    PODCASTS = "Podcasts"
    PROFILES = "Profiles"
    FEATURED_ON = "Featured on"
    FANS_MIGHT_ALSO_LIKE = "Fans might also like"


class ItemType(Enum):
    """
        Different types of items in YouTube Music
    """
    SONG = "Song"
    SINGLE = "Single"
    VIDEO = "Video"
    PLAYLIST = "Playlist"
    ALBUM = "Album"
    EP = "EP"
    ARTIST = "Artist"
    EPISODE = "Episode"
    PROFILE = "Profile"
    PODCAST = "Podcast"


class EndpointType(Enum):
    """
        Different type of endpoints in YouTube Music
    """
    WATCH_ENDPOINT = "watchEndpoint"
    BROWSE_ENDPOINT = "browseEndpoint"
    SEARCH_ENDPOINT = "searchEndpoint"
    URL_ENDPOINT = "urlEndpoint"


class IconType(Enum):
    """
        These are not yet used and represent the different types of icons 
        that can be found in YouTube Music.
    """
    ARTIST = "ARTIST"
    ALBUM = "ALBUM"
    SHARE = "SHARE"
    FLAG = "FLAG"
    MIX = "MIX"
    REMOVE = "REMOVE"
    QUEUE_PLAY_NEXT = "QUEUE_PLAY_NEXT"
    FAVORITE = "FAVORITE"
    UNFAVORITE = "UNFAVORITE"
    ADD_TO_REMOTE_QUEUE = "ADD_TO_REMOTE_QUEUE"
    ADD_TO_PLAYLIST = "ADD_TO_PLAYLIST"


class TextDivisorType(Enum):
    """
        Different types of text dividers. They are generally found 
        within the subtitles of the items.
    """
    BULLET_POINT = '\u2022'
