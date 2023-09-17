import requests
from bs4 import BeautifulSoup
import re
import os
import logging


"""
## Notion Watch List Metadata Updater
This python script will do the following:
1. Get Notion database items and filter for items with either an empty Title or Poster field.
2. For each matching item, query IMDB for the movie details.
3. Update the Notion database item with the movie details.

The script assumes you have a notion database with at least the following columns:
- Title (the title of the movie)
- Link (the imdb link to the movie)
- Poster (a link to the poster image for the movie)
- Genres (a list of genres the movie belongs to)
You can add any other columns you wish to your Notion database, as long as it has at least the above columns.

How to use:
1. Make sure your API key and Notion database ID are available to python as environment variables.
2. Browse IMDB and find movies or TV shows you want to add to your watch list.
3. Copy the IMDB url for each movie or TV show you want to add to your watch list, and paste it in the Link column of your Notion database.
4. Run this script. It will query your Notion database for any items with an empty Title or Poster field, and update them with the movie details from IMDB.
"""

# You need to provide your own Notion API token and database ID here
# Constants
NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DB_ID")
DEBUG = False
NOTION_VERSION = "2022-06-28"

# Setup logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

# Common headers for Notion API
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": NOTION_VERSION,
    "Content-Type": "application/json",
    "User-Agent": "Notion Watch List Metadata Updater",
}


def get_notion_database(databaseId: str) -> dict:
    """
    Query the Notion database for items with an empty Title or Poster field.

    Parameters:
    - databaseId: the ID of the Notion database to query

    Returns:
    - a dict containing the results of the query
    """
    data = {
        "filter": {
            "or": [
                {"property": "Title", "title": {"is_empty": True}},
                {"property": "Poster", "url": {"is_empty": True}},
            ]
        }
    }
    response = requests.post(
        f"https://api.notion.com/v1/databases/{databaseId}/query",
        headers=NOTION_HEADERS,
        json=data,
    )

    response.raise_for_status()
    return response.json()


def get_movie_details(imdb_link: str) -> tuple:
    """
    Get the details of the movie/tv show from IMDB.

    Parameters:
    - imdb_link: the IMDB link to the movie/tv show

    Returns:
    - a tuple containing the title, poster image link, formatted IMDB link, and a 
    list of genres the movie belongs to
    """
    logging.info(f"Getting movie details for {imdb_link}")
    imdb_id = re.search(r"tt\d+", imdb_link).group()
    formatted_imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    page = requests.get(formatted_imdb_url, headers=NOTION_HEADERS)
    if page.status_code != 200:
        logging.error(f"Failed to get movie details for {imdb_link}")
        logging.error(f"Response code: {page.status_code}")
        logging.error(f"Response text: {page.text}")
        raise ConnectionError(f"Failed to get movie details for {imdb_link}")
    soup = BeautifulSoup(page.content, "html.parser")
    title_html = soup.find_all("h1")
    if not title_html:
        raise ValueError(f"No title found for IMDB link: {imdb_link}")
    title = title_html[0].text

    poster_img_html = soup.find_all("meta", property="og:image")
    if not poster_img_html:
        raise ValueError(f"No poster image found for IMDB link: {imdb_link}")
    poster_image = poster_img_html[0].get("content")

    genre_tags = soup.find_all("span", class_="ipc-chip__text")
    if not genre_tags:
        raise ValueError(f"No genres found for IMDB link: {imdb_link}")
    formatted_genre_tags = []
    for tag in genre_tags:
        if "Back to top" not in tag.text:
            formatted_genre_tags.append(tag.text)

    logging.debug(f"imdb_id: {imdb_id}")
    logging.debug(f"formatted_imdb_url: {formatted_imdb_url}")
    logging.debug(f"response code: {page.status_code}")
    logging.debug(f"{title}, {poster_image} ({formatted_genre_tags})")

    return title, poster_image, formatted_imdb_url, formatted_genre_tags


def query_notion_database(databaseId: str, link: str) -> dict:
    """
    Query the Notion database for items with a matching IMDB link.
    Not currently used in the main workflow.

    Parameters:
    - databaseId: the ID of the Notion database to query
    - link: the IMDB link to query for

    Returns:
    - a dict containing the results of the query
    """
    data = {"filter": {"or": [{"property": "Link", "rich_text": {"contains": link}}]}}
    response = requests.post(
        f"https://api.notion.com/v1/databases/{databaseId}/query",
        headers=NOTION_HEADERS,
        json=data,
    )
    response.raise_for_status()
    return response.json()


def update_notion_page(pageId: str, title: str, poster_link: str, genre_tags) -> str:
    # removed type hint for genre_tags because it's not supported in the python
    # version running on the cloud function
    """
    Update the Notion database item with the movie details from IMDB.

    Parameters:
    - pageId: the ID of the Notion database item to update
    - title: the title of the movie/tv show
    - poster_link: the link to the poster image for the movie/tv show
    - genre_tags: a list of genres the movie belongs to

    Returns:
    - a string success message
    """
    data = {
        "properties": {
            "Poster": {"url": poster_link},
            "Title": {"title": [{"text": {"content": title}}]},
            "Genres": {"rich_text": [{"text": {"content": ", ".join(genre_tags)}}]},
        },
        "cover": {"type": "external", "external": {"url": poster_link}
        }
    }
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{pageId}", headers=NOTION_HEADERS, json=data
    )
    logging.debug(response.text)
    response.raise_for_status()
    return f"Success: updated {title} at {pageId}"



if __name__ == "__main__":
    results = get_notion_database(NOTION_DATABASE_ID, NOTION_TOKEN)

    if results["results"]:
        for result in results["results"]:
            try:
                movie_id = result["properties"]["Link"]["url"]
                database_entry_id = result['id']
                logging.debug(f"database_entry_id: {database_entry_id}")
                logging.info(f"movie_id to be updated: {movie_id}")
                logging.info(f"database_entry_id to be updated: {database_entry_id}")
                title, poster_image, formatted_imdb_url, genres = get_movie_details(movie_id)
                update_db_response = update_notion_page(
                    database_entry_id, title, poster_image, genres
                )
                logging.info(update_db_response)
            except Exception as e:
                logging.error(f"Error processing movie {movie_id}: {str(e)}")
                raise e
    else:
        logging.info("No movies needing updates found...")
