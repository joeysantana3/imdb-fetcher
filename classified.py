import requests
from bs4 import BeautifulSoup
import re
import os
import logging


class WatchlistUpdater:
    def __init__(self):
        self.notion_token = os.environ.get("NOTION_API_KEY")
        self.notion_database_id = os.environ.get("NOTION_DB_ID")
        self.debug = False
        self.notion_version = "2022-06-28"
        self.notion_headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json",
            "User-Agent": "Notion Watch List Metadata Updater",
        }
        self.entries_to_update = None

        logging.basicConfig(level=logging.DEBUG if self.debug else logging.INFO)

    def get_notion_database(self) -> dict:
        """
        Query the Notion database for items with an empty Title or Poster field.

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
            f"https://api.notion.com/v1/databases/{self.notion_database_id}/query",
            headers=self.notion_headers,
            json=data,
        )

        response.raise_for_status()
        return response.json()

    def get_movie_details(self, imdb_link: str) -> tuple:
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
        page = requests.get(formatted_imdb_url, headers=self.notion_headers)
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

    def query_notion_database(self, link: str) -> dict:
        """
        Query the Notion database for items with a matching IMDB link.
        Not currently used in the main workflow.

        Parameters:
        - link: the IMDB link to query for

        Returns:
        - a dict containing the results of the query
        """
        data = {
            "filter": {"or": [{"property": "Link", "rich_text": {"contains": link}}]}
        }
        response = requests.post(
            f"https://api.notion.com/v1/databases/{self.notion_database_id}/query",
            headers=self.notion_headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()

    def update_notion_page(
        self, pageId: str, title: str, poster_link: str, genre_tags
    ) -> str:
        # removed type hint for genre_tags because type list[str] is not supported
        # in the python version running on the cloud function
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
            "cover": {"type": "external", "external": {"url": poster_link}},
        }
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{pageId}",
            headers=self.notion_headers,
            json=data,
        )
        logging.debug(response.text)
        response.raise_for_status()
        return f"Success: updated {title} at {pageId}"


if __name__ == "__main__":
    updater = WatchlistUpdater()
    results = updater.get_notion_database()
    if results["results"]:
        for result in results["results"]:
            movie_id = result["properties"]["Link"]["url"]
            database_entry_id = result["id"]
            logging.debug(f"database_entry_id: {database_entry_id}")
            logging.info(f"movie_id to be updated: {movie_id}")
            logging.info(f"database_entry_id to be updated: {database_entry_id}")
            title, poster_image, _, formatted_genre_tags = updater.get_movie_details(
                movie_id
            )
            updater_response = updater.update_notion_page(
                database_entry_id, title, poster_image, formatted_genre_tags
            )
            logging.info(updater_response)
    else:
        logging.info("Nothing found to update.")
