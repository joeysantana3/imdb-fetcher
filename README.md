# Notion Automation Functions

## TODO
- Update to using the [class based verision](classified.py)


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
- Title (the title of the movie, will be filled by script)
- Link (the imdb link to the movie, you must paste in the link)
- Poster (a link to the poster image for the movie, will be filled by the script)
- Genres (a list of genres the movie belongs to, will be filled by the script)

You can add any other columns you wish to your Notion database, as long as it has at least the above four.

### How to use it.

1. Make sure your API key and Notion database ID are available to python as environment variables.
2. Browse IMDB and find movies or TV shows you want to add to your watch list.
3. Copy the IMDB url for each movie or TV show you want to add to your watch list, and paste it in the Link column of your Notion database.
4. Run this script. It will query your Notion database for any items with an empty Title or Poster field, and update them with the movie details from IMDB.

### Deploy the job to the cloud.

This script is much more useful and conveinent when it's run in the cloud and doesn't require any manual intervention or your local computer be up and running. There are many services out there that will do this, but [Render](https://render.com) is the easiest in my opinion. They have a [cronjob](https://render.com/docs/cronjobs) function that is perfect for this.

You could also use another serverless/function based service of your choice (for example, AWS Lambda).

1. Go to https://render.com
2. Create an account.
3. Create a new cron job.
4. Connect your github account
5. Add your environment vars to the cron job using the Render UI.
6. Deploy

### Demo
https://github.com/joeysantana3/imdb-fetcher/assets/40314133/c7b3a909-08ec-476e-a42f-1263449c4a8f

### Dashboard/Poster View in Notion
![poster_view](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/626ffd56-06f5-405b-bcfc-a6646e04aa8a)


