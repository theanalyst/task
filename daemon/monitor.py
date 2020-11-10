#import aiohttp
import asyncio
import logging 
import time

from aiohttp import ClientSession, TCPConnector, ClientTimeout

LOG_FORMAT='%(asctime)-15s %(message)s'
logging.basicConfig(format=LOG_FORMAT)

def default_int(val, default_val):
  try:
    v = int(val)
  except ValueError:
    logger.error('Exception convertiong int %s', val)
    v = default_val
  return v

class AsyncMonitorDaemon():
  """A simple async aiohttp client that can at present do GET requests on a uri"""

  def __init__(self, endpoint, count = 10, sleep_time=10, debug=False):
      self.logger = logging.getLogger('mag-mon')  # Magnificent Monitor!
      if debug:
        self.logger.setLevel(logging.DEBUG)
      self.endpoint = endpoint
      self.req_count = count  # parallel async req
      self.sleep_time = default_int(sleep_time, 10)

  async def fetch(self, session):
    """ A simple fetch uri method that async fetches an endpoint"""
    async with session.get(self.endpoint) as resp:
      if resp.status != 200:
        self.logger.error('Magnificent req error, status=%d', resp.status)
        return await resp.read() # Not consumed so can be dropped atm
   
  async def multi_fetch(self):
    reqs = []
    timeout = ClientTimeout(total=300)
    # TODO reuse sessions more creatively
    while True:
      async with ClientSession(connector=TCPConnector(keepalive_timeout=600), timeout=timeout) as session:
        for i in range(self.req_count):
          self.logger.debug('making req')
          reqs.append(asyncio.ensure_future(
            self.fetch(session)
          ))
        
        resps = await asyncio.gather(*reqs)
        await asyncio.sleep(self.sleep_time)
    
  def run(self, ev_loop):
    future = asyncio.ensure_future(self.multi_fetch())
    ev_loop.run_until_complete(future)
