import uvicorn
from fastapi import FastAPI
from starlette.responses import Response
import news
from pydantic import BaseModel

app = FastAPI()

class Article(BaseModel):
    id: str
    title: str
    url: str
    datetime: str


@app.get('/articles')
def get_articles() -> list[Article]:
    articles = news.scrape()

    return [ Article(**a) for a in articles 
        if 'title' in a and 'url' in a and 'datetime' in a and 'id' in a]


class SingleArticle(BaseModel):
    title: str
    headline: str
    labels: list[str]


@app.get('/articles/{id}')
def get_article(id: str) -> SingleArticle:
    all_articles = news.scrape()
    found = None
    for a in all_articles:
        if a['id'] == id:
            found = a

    return SingleArticle(**news.scrape_contents(found['url']))

if __name__ == '__main__':
    uvicorn.run('asgi:app', port=3000, reload=True)
