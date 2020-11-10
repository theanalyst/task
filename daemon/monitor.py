#import aiohttp
import asyncio
import logging 
import time

from aiohttp import ClientSession, TCPConnector, ClientTimeout

LOG_FORMAT='%(asctime)-15s %(levelname)s %(message)s'
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

  def __init__(self, endpoint, count = 10, sleep_time=10, debug=False, log_file='mon.log'):
      self.logger = logging.getLogger('mag-mon')  # Magnificent Monitor!
      if debug:
        self.logger.setLevel(logging.DEBUG)
      fh = logging.FileHandler(log_file)
      self.logger.addHandler(fh)

      self.endpoint = endpoint
      self.req_count = default_int(count, 10)  # parallel async req
      self.sleep_time = default_int(sleep_time, 10)

  async def fetch(self, session):
    """ A simple fetch uri method that async fetches an endpoint"""
    async with session.get(self.endpoint) as resp:
      if resp.status != 200:
        self.logger.error('Magnificent req error, status=%d', resp.status)
        return await resp.read() # Not consumed so can be dropped atm
   
  async def multi_fetch(self):
    """A method that reuses a session to fire off multiple requests and
    wait for a specified time after to fire the next batch. The number of parallel requests is governed     by req_count & time to wait by sleep_time """
    reqs = []
    timeout = ClientTimeout(total=300)
    async with ClientSession(connector=TCPConnector(keepalive_timeout=600), timeout=timeout) as session:
      req_ctr = 0
      while True:
        start = time.perf_counter()
        for i in range(self.req_count):
          self.logger.debug('firing off req %d', req_ctr)
          reqs.append(asyncio.ensure_future(
            self.fetch(session)
          ))
          req_ctr = ctr+1

        resps = await asyncio.gather(*reqs)
        end = time.perf_counter()
        t = end -start
        self.logger.debug('%d reqs took %s s', self.req_count, t)
        await asyncio.sleep(self.sleep_time)
    
  def run(self, ev_loop):
    future = asyncio.ensure_future(self.multi_fetch())
    ev_loop.run_until_complete(future)
