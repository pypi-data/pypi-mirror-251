# InnerTube Data Extractor (ITDE)
![Version](https://img.shields.io/badge/version-1.0.4-blue)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://en.wikipedia.org/wiki/MIT_License)


ITDE is a Python-based tool designed to extract valuable information, including multimedia content and associated metadata, from the data provided by InnerTube, Google's private API. 
InnerTube serves as a comprehensive source of data, and ITDE empowers developers to seamlessly retrieve and organize essential details from this platform.

### Features

- **Organized Data Structures:**  ITDE efficiently organizes extracted data in a structured and typed manner.
- **Versatility:** Designed to handle various types of multimedia content.
- **Python Compatibility:** Written in Python, making it accessible and easy to integrate into existing projects.

### Installation
```shell
pip install itde
```


### Usage
```python
# Python Client for Google's Private InnerTube API
from innertube import InnerTube

# Module for extraction
from itde import extractor

# Construct a client
client = InnerTube('WEB_REMIX')

# Get data
data = client.search('Squarepusher')

# Extract data. 
extracted_data = extractor.extract(data)
```

Once the data has been extracted, it can be processed.

```python
from itde import ItemsContainer
from itde import ShelfContainer

# Print basic information about the extracted data
print(f"Extracted Data Type: {type(extracted_data)}")
print(f"Number of Items or Shelves: {len(extracted_data)}")

# The following code is intended only to provide a quick 
# overview of the data structure provided by the extracted method

# Display detailed information about the extracted data
if isinstance(extracted_data, ItemsContainer):
    print("\nItems Container:")
    for item in extracted_data:
        print(f"  Type:          {item.type}")
        print(f"  Name:          {item.name}")
        print(f"  Endpoint:      {item.endpoint}")
        print(f"  Thumbnail url: {item.thumbnail_url}")

elif isinstance(extracted_data, ShelfContainer):
    print("\nShelf Container:")
    for shelf in extracted_data:
        print(f"  Type:     {shelf.type}")
        print(f"  Endpoint: {shelf.endpoint}")
        for item in shelf:
            print(f"    Type:          {item.type}")
            print(f"    Name:          {item.name}")
            print(f"    Endpoint:      {item.endpoint}")
            print(f"    Thumbnail url: {item.thumbnail_url}")

# Depending on the type of item, additional data may be present 
# such as release date, view, subscribers, etc.
```

For a more in-depth understanding of the data structure and usage, refer to the example scripts provided in the examples directory. These examples demonstrate how to work with ItemsContainer and ShelfContainer and can serve as a reference for exploring the capabilities of ITDE.

## Disclaimer

**Note:** ITDE heavily relies on data provided by InnerTube. The reliability and functionality of this code may vary over time, as they are subject to any changes or updates made by InnerTube's data structure or API.

Please keep in mind the following:

- The codebase is designed to adapt to potential changes in InnerTube's data format.
- It's recommended to stay updated with any releases or announcements related to ITDE.

## Status

⚠️ **Work in Progress:** This repository is currently in a state that requires additional development and may not include all intended features. While the core functionality is present, small improvements and additional features are planned for future releases.

Feel free to contribute, report issues, or check back for updates as we continue to enhance and expand ITDE.

Your contributions and feedback are highly appreciated to help maintain and improve the reliability of ITDE.
