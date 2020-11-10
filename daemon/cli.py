import argparse
import asyncio
import time

from monitor import AsyncMonitorDaemon

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monitor Magnificient')
    parser.add_argument('--uri', default='http://localhost:12345',
                        help='Magnificient server url')
    parser.add_argument('--reqs', default=10,
                        help='Concurrent reqs to fire')
    parser.add_argument('--sleep_time', default = 10,
                        help='time to sleep between requests')
    parser.add_argument('--debug', action='store_true',
                        help='debug logging')
    parser.add_argument('--log-file', default='mon.log',
                        help='log file for output')
    args = parser.parse_args()

    daemon = AsyncMonitorDaemon(args.uri, args.reqs, args.sleep_time, args.debug)
    loop = asyncio.get_event_loop()
    daemon.run(loop)
