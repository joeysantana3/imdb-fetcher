# Render
Render is my choice for cloud providers and has a great offering for running this script. It does cost money, but is pretty cheap.

You could also use other cloud provider's serverless offerings such as AWS Lambda or Azure Functions, but it's more complicated.

## Run this script in the cloud.
1. Go to https://render.com and sign up for account. You will likely need to enter in CC info.
2. Fork this repo into your github account.
3. On your Render dashboard, click "New" and choose "Cron job."
4. Choose "Build and deploy from a Git repository."
5. If you haven't already, connect your github account to Render.
6. Once your Github account is connected, you should see a list of your repositories in the "Create a new Cron Job" wizard. Click "Connect" on your forked copy of this repo.
7. Give it a name of your choosing.
8. Choose a schedule using cron notation. I do every 30 minutes which is `*/30 * * * *`
9. In the command section, type `python worker.py`.
10. Choose the least expensive instance to run your job.
11. Click "Advanced."
12. Click "Add Environment Variable."
13. The first one's key should be `NOTION_API_KEY` and it's value should be your API key from notion. (See [here](../main/docs/Notion-Info.md#integrationapi-key))
14. The second one's key should be `NOTION_DB_ID` and it's value should be your watchlist database id. (See [here](../main/docs/Notion-Info.md#watchlist-setup))
15. Click "Create Cron Job"
16. Run the job manually.
17. If successful, your notion database should have updated with the correct metadata for your IMDB link.
