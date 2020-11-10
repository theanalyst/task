import aiohttp
import asyncio
import logging 
import time

class AsyncMonitorDaemon():
  """A simple async aiohttp client that can at present do GET requests on a uri"""

  def __init__(self, endpoint, count = 10, sleep_time=10):
      self.logger = logging.getLogger('mag-mon')  # Magnificent Monitor!
      self.endpoint = endpoint
      self.req_count = 10  # parallel async req
      self.sleep_time = 10

  async def fetch(self):
    """ A simple fetch uri method that async fetches an endpoint"""
    async with aiohttp.ClientSession() as session:
        async with session.get(self.endpoint) as resp:
            if resp.status != 200:
                self.logger.error('Magnificent req error, status=%d', resp.status)
                return await resp.read() # Not consumed so can be dropped atm
   
  async def multi_fetch(self):
    reqs = []
    for i in range(self.req_count):
        reqs.append(asyncio.ensure_future(
            self.fetch()
        ))
        
    resps = await asyncio.gather(*reqs)

  def run(self, ev_loop):
    while True:
      future = asyncio.ensure_future(self.multi_fetch())
      ev_loop.run_until_complete(future)
      time.sleep(self.sleep_time)
