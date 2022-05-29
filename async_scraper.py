import asyncio
import aiohttp
import os
import time
import requests
from bs4 import BeautifulSoup
from parser import parser
from variables import *

from dotenv import load_dotenv
load_dotenv()

symbols = SYMBOLS
results = []
elements = ELEMENTS
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
url = URL
proxy_list = PROXY_LIST

def get_content_type(response):
    return response.headers.get('Content-Type')
    
def response_type_json(response):
    content_type = get_content_type(response)
    if 'json' in content_type:
        print('content is:json')
        return True
    return False

async def get_page(session,url,proxy=None):
    r = None
    try:
        async with session.get(url,proxy=proxy,ssl=False) as response:
            if response_type_json(response):
                return await response.json()
            else:
                return await response.text()
    except Exception as e:
        print(e)
        return None

async def start_requests(session,urls,proxylist=[]):
    tasks = []
    for count,url in enumerate(urls):
        proxy = proxylist[count] if len(proxylist) > count else None
        print('processing {}'.format(url))
        try:
            task = asyncio.create_task(get_page(session,url,proxy=proxy))
        except Exception as e:
            print("Request not sent")
            print(e)
            print(proxy)
            print(url)
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

def construct_url(url,symbol,api_key):
    return url.format(symbol,api_key)

async def main(urls):
    async with aiohttp.ClientSession() as session:
        data = await start_requests(session,urls,proxy_list)
        return data
        
if __name__ == '__main__':
    urls = [construct_url(url,symbol,api_key) for symbol in symbols]

    start = time.time()
    print('timer started')
    results = asyncio.run(main(urls))
    end = time.time()

    total_time = end-start
    print(f'it took {total_time} seconds to make {len(results)} api calls')
    
    for res in results:
        data = parser(res)
        print(data)
