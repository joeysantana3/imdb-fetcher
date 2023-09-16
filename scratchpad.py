import requests
from bs4 import BeautifulSoup
import logging
import re


logging.basicConfig(level=logging.DEBUG)


def get_movie_details(imdb_link: str) -> tuple:
    """
    Get the details of the movie/tv show from IMDB.

    Parameters:
    - imdb_link: the IMDB link to the movie/tv show

    Returns:
    - a tuple containing the title, poster image link, and a formatted IMDB link
    """
    logging.info(f"Getting movie details for {imdb_link}")
    imdb_id = re.search(r"tt\d+", imdb_link).group()
    formatted_imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    page = requests.get(formatted_imdb_url, headers={"User-Agent": "Mozilla/5.0"})
    if page.status_code != 200:
        logging.error(f"Failed to get movie details for {imdb_link}")
        logging.error(f"Response code: {page.status_code}")
        logging.error(f"Response text: {page.text}")
        return None, None, None
    soup = BeautifulSoup(page.content, "html.parser")
    title_html = soup.find_all("h1")
    if not title_html:
        raise ValueError(f"No title found for IMDB link: {imdb_link}")
    title = title_html[0].text

    poster_img_html = soup.find_all("meta", property="og:image")
    if not poster_img_html:
        raise ValueError(f"No poster image found for IMDB link: {imdb_link}")
    poster_image = poster_img_html[0].get("content")

    formatted_genre_tags = []
    genre_tags = soup.find_all("span", class_="ipc-chip__text")
    for tag in genre_tags:
        if "Back to top" not in tag.text:
            formatted_genre_tags.append(tag.text)

    print("\n\n\n")
    print(formatted_genre_tags)
    print("\n\n\n")
    logging.debug(f"imdb_id: {imdb_id}")
    logging.debug(f"formatted_imdb_url: {formatted_imdb_url}")
    logging.debug(f"response code: {page.status_code}")
    logging.debug(f"{title}, {poster_image}")

    return title, poster_image, formatted_imdb_url


get_movie_details("https://www.imdb.com/title/tt13622776/?ref_=ttls_li_tt")
