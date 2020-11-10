import aiohttp
import asyncio
import logging 
import time

class AsyncMonitorDaemon():
  """A simple async aiohttp client that can at present do GET requests on a uri"""

  def __init__(self, endpoint, count = 10):
      self.logger = logging.getLogger('mag-mon')  # Magnificent Monitor!
      self.endpoint = endpoint
      self.req_count = 10  # parallel async req

  async def fetch(self): 
    async with aiohttp.ClientSession() as session:
        async with session.get(self.endpoint) as resp:
            if resp.status != 200:
                self.logger.error('req error, status=%d', resp.status)
                return await resp.read() # Not consumed so can be dropped atm
   
  async def run(self):
    reqs = []
    for i in range(self.req_count):
        reqs.append(asyncio.ensure_future(
            self.fetch()
        ))
        
    resps = await asyncio.gather(*reqs)
          
