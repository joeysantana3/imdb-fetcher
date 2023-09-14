
## Notion Movie Watch List Metadata Updater

I wrote this script to help me manage my Movie and TV Show watchlist in Notion. I can browse IMDB for content I want to watch, paste the IMDB link to my Notion database, then this script updates the database with things like the title of the movie and a link to the poster image.

The script can be modified to extract and update more infomration, such as release dates.

NOTICE: This script relies on the HTML structure of an IMDB page to stay as it was when the script was written. If IMDB changes their page layout, this will break.

### What it does.
1. Get Notion database items and filter for items with either an empty Title or Poster field.
2. For each matching item, query IMDB for the movie details.
3. Update the Notion database item with the movie details.

### What are the prerequisites.

The script assumes you have a notion database with at least the following columns:
- Title (the title of the movie)
- Link (the imdb link to the movie)
- Poster (a link to the poster image for the movie)

You can add any other columns you wish to your Notion database, as long as it has the above three.

### How to use it.

1. Make sure your API key and Notion database ID are available to python as environment variables.
2. Browse IMDB and find movies or TV shows you want to add to your watch list.
3. Copy the IMDB url for each movie or TV show you want to add to your watch list, and paste it in the Link column of your Notion database.
4. Run this script. It will query your Notion database for any items with an empty Title or Poster field, and update them with the movie details from IMDB.

### Demo
