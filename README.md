## NetEase Music Search Engine

**Keep in contact: Please contact me in github if there are any problems**

### Function

This program is used for general retieval for NetEase musics, with beta1 implementation prototype as a course project. The search engine offers retieval functions as follows:

1. Input the name of an artist, return a ranked list of artist homepages and music pages;
2. Input the title of a music, return a ranked list of music pages;
3. Input a keyword about an artist or a music, return a ranked list of relevant pages;
4. Optimize return results by collecting user interest in page choices.
5. TO BE DONE ...


### Framework

The framework of such a search engine is mainly divided into three parts:

1. **Crawler**: craw all useful information from the source website
    - spider:
        - CrawArtist: craw artist information by artist_id
        - CrawAlbum: craw album information by album_id related to artist_id
        - CrawMusic: craw music information by music_id related to album_id
        - CrawComment: craw comment information related to  music_id
    - sql:
        - sql: Store raw information into database in order

2. **Index Builder**: build an index database/data structure according to the raw database
    - index:
        - Splitter: split contents into terms according to the raw information
        - WeightManager: compute the weight of each page correlated to each term and rank them in a page list
        - Indexer: construct and save index data structure
    - sql:
        - sql: Extract all useful information for building index 

3. **Retriever**; search indexer and return ranked pages according to the user input
i   - retriever:
    - Splitter: split user input
    - Searcher: search in indexer and return matched pages in order

### GUI Prettifier

TO BE DONE here ...
