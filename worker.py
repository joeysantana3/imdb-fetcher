import requests
from bs4 import BeautifulSoup
import re
import os


"""
## Notion Watch List Metadata Updater
This python script will does the following:
1. Get Notion database items and filter for items with either an empty Title or Poster field.
2. For each matching item, query IMDB for the movie details.
3. Update the Notion database item with the movie details.

The script assumes you have a notion database with at least the following columns:
- Title (the title of the movie)
- Link (the imdb link to the movie)
- Poster (a link to the poster image for the movie)
You can add any other columns you wish to your Notion database, as long as it has the above three.

How to use:
1. Make sure your API key and Notion database ID are available to python as environment variables.
2. Browse IMDB and find movies or TV shows you want to add to your watch list.
3. Copy the IMDB url for each movie or TV show you want to add to your watch list, and paste it in the Link column of your Notion database.
4. Run this script. It will query your Notion database for any items with an empty Title or Poster field, and update them with the movie details from IMDB.
"""

# You need to provide your own Notion API token and database ID here
NOTION_TOKEN = os.environ.get("NOTION_API_KEY")
NOTION_DATABASE_ID = os.environ.get("NOTION_DB_ID")
DEBUG = True


# 1. get the database items which have either an empty Title or Poster
def get_notion_database(databaseId: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
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
        headers=headers,
        json=data,
    )

    if response.status_code == 200:
        return response.json()
    else:
        return (
            f"Request failed with status code {response.status_code}, {response.text}"
        )


def get_movie_details(imdb_link: str) -> tuple:
    print(f"Getting movie details for {imdb_link}")
    imdb_id = re.search(r"tt\d+", imdb_link).group()
    formatted_imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
    }
    page = requests.get(formatted_imdb_url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    title_html = soup.find_all("h1")
    title = title_html[0].text
    poster_img_html = soup.find_all("meta", property="og:image")
    poster_image = poster_img_html[0].get("content")

    if DEBUG:
        print(f"imdb_id: {imdb_id}")
        print(f"formatted_imdb_url: {formatted_imdb_url}")
        print(f"response code: {page.status_code}")
        print(title, poster_image)

    return title, poster_image, formatted_imdb_url


# 3. Query the Notion database
def query_notion_database(databaseId: str, link: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    data = {"filter": {"or": [{"property": "Link", "rich_text": {"contains": link}}]}}
    response = requests.post(
        f"https://api.notion.com/v1/databases/{databaseId}/query",
        headers=headers,
        json=data,
    )
    return response.json()


# 4. Update the Notion database item
def update_notion_page(pageId: str, title: str, poster_link: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    data = {
        "properties": {
            "Poster": {"url": poster_link},
            "Title": {"title": [{"text": {"content": title}}]},
        }
    }
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{pageId}", headers=headers, json=data
    )

    if response.status_code == 200:
        return f"Success: updated {title} at {pageId}"
    else:
        return (
            f"Request failed with status code {response.status_code}, {response.text}"
        )


# Get database items with either no title or poster link
results = get_notion_database(NOTION_DATABASE_ID, NOTION_TOKEN)
# get the details for each movie
if results["results"]:
    for result in results["results"]:
        movie_id = result["properties"]["Link"]["url"]
        database_entry_id = result["url"].split("/")[-1]
        print(f"movie_id's to be updated: {movie_id}")
        print(f"database_entry_id's to be updated: {database_entry_id}")
        title, poster_image, formatted_imdb_url = get_movie_details(movie_id)
        # update_notion_page
        update_db_response = update_notion_page(
            database_entry_id, title, poster_image, NOTION_TOKEN
        )
        print(update_db_response)
else:
    print("No movies needing updates found...")
