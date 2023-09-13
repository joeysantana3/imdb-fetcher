I'm attempting to use [pipedream](https://pipedream.com) as a way to automate updating the info. I have a basic task working that I'm going to copy here.

Pipedream works by configuring tasks as blocks. Each tasks has an output that you can then use in the next task.



## 1. Trigger
The trigger is just dropdown selects. You pick your notion account, how often you want this "script" to run, and the database you want to monitor.

- Notion Account: dropdown select
- Timer: choose how often, dropdown select
- Database ID: Watch List Database, dropdown select

## 2. code (python)
The first step after the trigger is using python to grab the details from imdb. Notice the function is named "handler" and accepts "pd: 'pipedream'". This is required in order for A) the function to run and B) the data from notion to be available.

The return data will be sent to the next step.

```python
import requests
from bs4 import BeautifulSoup
import re

DEBUG = True

def handler(pd: "pipedream") -> tuple:
    imdb_link = pd.steps["trigger"]["event"]["properties"]["Link"]["url"]
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

    return title, poster_image, formatted_imdb_url
```

## 3. Notion
The preconfigured notion task on this service is a javascript task, so I switched to using js here.

The second step is to query the notion database for the object you are working on and grab the specific database item by it's id. In notion, database items are just pages.

- Notion Account: dropdown select
```javascript
import { axios } from "@pipedream/platform"
export default defineComponent({
  props: {
    notion: {
      type: "app",
      app: "notion",
    }
  },
  async run({steps, $}) {
    const databaseId = steps.trigger.event.parent.database_id
    const title = steps.code.$return_value[0]
    const poster_link = steps.code.$return_value[1]

    const response = await axios($, {
      method: 'POST',
      url: `https://api.notion.com/v1/databases/${databaseId}/query`,
      headers: {
        Authorization: `Bearer ${this.notion.$auth.oauth_access_token}`,
        "Notion-Version": `2022-06-28`,
        "Content-Type": "application/json"
      },
      data: {
        filter : {
          or: [
            {
            property: "Link",
            rich_text: {
              contains: steps.code.$return_value[2]
            }
            }
          ]
        }
      }
    })
    return {
      title: title,
      poster_link: poster_link,
      notionResponse: response
      }
  },
})
```

## 4. Notion
Step 3 is to update the database item. Update the title and poster fields with data pulled from imdb. That way, all we have to do is enter a link in the notion database, then when this runs the title and the poster will be updated.

- Notion Account: dropdown select
```javascript
import { axios } from "@pipedream/platform"
export default defineComponent({
  props: {
    notion: {
      type: "app",
      app: "notion",
    }
  },
  async run({steps, $}) {
    const pageId = steps.notion.$return_value.notionResponse.results[0].id
    return await axios($, {
      method: 'PATCH',
      url: `https://api.notion.com/v1/pages/${pageId}`,
      headers: {
        Authorization: `Bearer ${this.notion.$auth.oauth_access_token}`,
        "Notion-Version": `2022-06-28`,
        "Content-Type": "application/json"
      },
      data: {
        "properties": {
          "Poster": {
            "url": steps.notion.$return_value.poster_link
          },
          "Title": {
            "title": [
              {
                "text":{
              "content": steps.notion.$return_value.title
                }
              }
            ]
          }
        }
      }
    })
  }
})
```
