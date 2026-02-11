from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool
from app.schema.preprocess import Article
from app.services.preprocessing.article_preprocessing import ready_data
import requests


url = "https://advances-involves-roll-leads.trycloudflare.com/api/v1/coref"
router = APIRouter()

@router.post("/preprocess")
async def preprocess(data: Article):
    json_result = await run_in_threadpool(ready_data, data)
    payload = {'content': json_result['content'], "url": json_result['url']}

    response = requests.post(url, json=payload)

    return response.json()

