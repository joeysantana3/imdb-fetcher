
import requests
from bs4 import BeautifulSoup
import re

DEBUG = True

def get_imdb_title_poster(imdb_link: str) -> tuple:
    imdb_id = re.search(r'tt\d+', imdb_link).group()
    formatted_imdb_url = f'https://www.imdb.com/title/{imdb_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
    }
    page = requests.get(formatted_imdb_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_html = soup.find_all('h1')
    title = title_html[0].text
    poster_img_html = soup.find_all('meta', property="og:image")
    poster_image = poster_img_html[0].get("content")

    if DEBUG:
        print(f"imdb_id: {imdb_id}")
        print(f"formatted_imdb_url: {formatted_imdb_url}")
        print(f"response code: {page.status_code}")
        print(title, poster_image)

    return title, poster_image

if __name__ == "__main__":
    user_input = input("Enter IMDB link: ")
    get_imdb_title_poster(user_input)
