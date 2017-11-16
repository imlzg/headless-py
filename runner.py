import asyncio
import logging

from pyppeteer.launcher import launch
from pyppeteer.network_manager import NetworkManager
from pyppeteer.network_manager import Response
from pyppeteer.page import Page


async def req_callback(request):
    print("[request] {0} {1}".format(request.method, request.url))


async def fin_callback(request):
    response = request.response
    if 300 < response.status < 310:
        text_content = "Redirect..."
    else:
        try:
            text_content = await response.buffer()
        except:
            text_content = "Failed"

    print("[response] {0} {1}... (Data: {2}...)".format(response._request.method, response._request.url[:100], text_content[:10]))


async def security_callback(event):
    print("[security state changed] {0}".format(event))


async def err_callback(*args, **kwargs):
    print("[err] {0} {1}".format(args, kwargs))


async def main(browser):
    page = await browser.newPage()
    page.on(NetworkManager.Events.Request, req_callback)
    page.on(NetworkManager.Events.RequestFinished, fin_callback)
    page.on(Page.Events.SecurityStateChanged, security_callback)
    page.on('error', err_callback)

    await page.setViewport({'width': 1920, 'height': 1080})
    await page.goto('https://msn.com/', {'timeout': 10000, 'networkIdleTimeout': 10000})
    await page.screenshot({'path': 'screenshot.png'})


browser = launch()
asyncio.get_event_loop().run_until_complete(main(browser))

# google-chrome --headless --disable-gpu --screenshot=test.png http://www.google.com --no-sandbox)


"""

Traceback (most recent call last):
  File "/usr/local/lib/python3.6/asyncio/events.py", line 127, in _run
    self._callback(*self._args)
  File "/usr/local/lib/python3.6/site-packages/pyee/__init__.py", line 159, in _callback
    self.emit('error', exc)
  File "/usr/local/lib/python3.6/site-packages/pyee/__init__.py", line 168, in emit
    raise args[0]
  File "test.py", line 13, in res_callback
    text_content = await response.buffer()
  File "/usr/local/lib/python3.6/site-packages/pyppeteer/network_manager.py", line 286, in _bufread
    'requestId': self._request._requestId
  File "/usr/local/lib/python3.6/site-packages/pyppeteer/connection.py", line 176, in send
    return await callback
pyppeteer.errors.NetworkError: Protocol Error: No data found for resource with given identifier None


"""