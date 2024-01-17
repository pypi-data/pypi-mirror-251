import logging
import os
import sys
import unittest
import json
from innertube import InnerTube  # type: ignore
from datetime import datetime
from typing import Optional
from typing import Dict
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from itde import ItemsContainer   # noqa
from itde import ShelfContainer   # noqa
from itde import Item             # noqa
from itde import extractor        # noqa


logger = logging.getLogger(__name__)


class TestExtractor(unittest.TestCase):

    def setUp(self) -> None:
        self.client = InnerTube('WEB_REMIX')

    def test_extract_search_data(self) -> None:
        for query in [
            'Squarepusher',
            'Aphex Twin',
            'saf;jaksdfj;asdkfjakgj',
            'Boh',
            'Testing',
            'Another one',
            'Travis Scott'
        ]:
            data = self.client.search(query)
            # _save_data("search", data)
            extracted_data = extractor.extract(data)
            _check_extracted_data_integrity(extracted_data)
            _print_shelf_container(extracted_data)

    def test_extract_browse_artist_data(self) -> None:
        data = self.client.browse('UCpwax2-MvnILOcR68QWOZ1g')
        # _save_data("browse_artist", data)
        extracted_data = extractor.extract(data)
        _check_extracted_data_integrity(extracted_data)
        _print_shelf_container(extracted_data)

    def test_extract_browse_album_data(self) -> None:
        data = self.client.browse('MPADUCpwax2-MvnILOcR68QWOZ1g')
        # _save_data("browse_album", data)
        extracted_data = extractor.extract(data)
        _check_extracted_data_integrity(extracted_data)
        _print_items_container(extracted_data)

    def test_extract_next_content_data(self) -> None:
        data = self.client.next(playlist_id='RDCLAK5uy_lOLCULJgoSlAgxiG4C3yl07S7R4O3DuN4')
        # _save_data("next", data)
        extracted_data = extractor.extract(data)
        _check_extracted_data_integrity(extracted_data)
        _print_items_container(extracted_data)


def _check_extracted_data_integrity(extracted_data: Optional[List]) -> None:
    # TODO
    pass


def _check_item_data_integrity(item: Item) -> None:
    # TODO
    pass


def _save_data(file_type: str, data: Dict) -> None:
    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    filename = f"{file_type}_{now}.json"
    with open(os.path.join('innertube_response', filename), mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def _print_items_container(items_container: ItemsContainer) -> None:
    if items_container:
        print()
        print()
        print('TITLE:', items_container.name)
        for item in items_container:
            print(item)


def _print_shelf_container(shelf_container: ShelfContainer) -> None:
    if shelf_container:
        print()
        print()
        for shelf in shelf_container:
            print()
            print('TITLE:', shelf.type.value)
            print('ENDPOINT:', shelf.endpoint)
            for item in shelf:
                print(item)


if __name__ == "__main__":
    logger.level = logging.INFO
    logger.addHandler(logging.StreamHandler(sys.stdout))
    test_extractor = TestExtractor()
    test_extractor.setUp()
    test_extractor.test_extract_search_data()
    test_extractor.test_extract_browse_artist_data()
    test_extractor.test_extract_browse_album_data()
    test_extractor.test_extract_next_content_data()
