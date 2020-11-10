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

    args = parser.parse_args()

    daemon = AsyncMonitorDaemon(args.uri, args.reqs)
    loop = asyncio.get_event_loop()
    daemon.run(loop)
