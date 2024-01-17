import cachetools
import httpx
import ujson
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ronds_sdk import PipelineOptions


class HttpManager:
    def __init__(self, options: 'PipelineOptions'):
        self.http_port = options.http_port
        self.route = options.route
        self.address = options.address
        self.agreement = options.agreement
        self.path = options.path
        self.mode = options.mode
        self.cache = cachetools.TTLCache(maxsize=100, ttl=120)

    async def async_call_post_api(self, json):
        if json not in self.cache:
            self.cache[json] = await self.async_post(json)
        return self.cache[json]

    async def async_post(self, json):
        client = httpx.AsyncClient()
        async with client:
            result = {'data': None, 'exception': ''}
            json_param = ujson.loads(json)
            try:
                url = self.agreement + "://" + self.address + ":" + str(self.http_port) + self.route + self.path
                response = await client.post(url=str(url), json=json_param, timeout=50)
                if response.is_success:
                    result['data'] = response.json()
                else:
                    if response.status_code == 404:
                        result['exception'] = '404 ' + response.reason_phrase
                    else:
                        result['exception'] = str(response.status_code) + " " + response.text
            except Exception as ex:
                result['exception'] = str(response.status_code) + "Connect Timeout" + str(ex)
            finally:
                await client.aclose()
                return ujson.dumps(result)
