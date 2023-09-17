# Notion

At it's core, notion is a tool for taking notes. However, it offers a ton of advanced functionality over a normal note taking app. One of the features of Notion is databases. You can add a database in Notion and reference it from other places within your Notion workspace. It also offers an API which makes things like this script possible. Best of all, you can use it for free.

In this doc I'll walk you through how I set up my watchlist.

## Watchlist Setup
1. After you have created your account and logged in, create a new page.

![Screenshot from 2023-09-16 22-17-55](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/5ee469c1-0e5a-4f18-94ea-527e4d41baa7)

2. In your new page, after giving it a title, click into the body and type `/data`. Then choose "Database - Full Page."

![1](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/b4cdd87f-f88d-4fdd-a2a3-d86d4632758c)

3. In your new database, change the "Name" column to "Title", then add in Link(of type URL), Poster(of type URL), and Genres(of type text) columns. You can add other columns if you wish, such as "My Rating" or "Watched."

![Screenshot_2023-09-16_22-26-29](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/da8f6160-7ba7-4e2f-82e1-bf9e11c11da8)
![Screenshot from 2023-09-16 22-31-12](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/02fb5512-f0ad-43d4-a7a6-b1510fb6e2a8)

4. Copy down the ID of your new database from the URL. You just need the string between the `/` and the `?`. `ec2d1710659345c9b497303054936022` in this case.

![Screenshot from 2023-09-16 22-33-41](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/0eb6049f-f111-4a08-9db9-de8c947278cc)

5. Go to imdb.com and find a movie or TV show you want to add. Copy the full link to the page.

![Screenshot from 2023-09-16 22-37-22](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/45361909-36c3-4b3b-b645-79c6aea09741)

6. Paste the link to your new database. Choose an empty row and paste the link into the "Link" column.

![Screenshot from 2023-09-16 22-40-01](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/a88c3bc7-9f20-4603-a111-96e9cdf5f699)


## Integration/API Key

In order to get an API key for use with this script, follow these steps:
1. Go to https://www.notion.so/my-integrations/.
2. Click "+ New integraion."
3. Give it a name and leave everything else default.
4. Click "Submit ->."
5. On the next page, you should be presented with an "Internal Integration Secret." Copy that and save it. This is your API Key.

![Screenshot from 2023-09-16 22-45-50](https://github.com/joeysantana3/imdb-fetcher/assets/40314133/00ddad67-61d8-4323-930e-692ca233826e)
