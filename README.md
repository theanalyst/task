# README

This is a very simple http client that makes specified number of
concurrent requests every few seconds and logs error report

## INSTALL

This uses aiohttp package for async requests

	pip install aiohttp


## USAGE

	usage: python monitor/cli.py [-h] [--uri URI] [--reqs REQS] [--sleep_time SLEEP_TIME]
              [--debug] [--log-file LOG_FILE]

	Monitor Magnificient

	optional arguments:
	-h, --help            show this help message and exit
	--uri URI             Magnificient server url
	--reqs REQS           Concurrent reqs to fire
	--sleep_time SLEEP_TIME
                        time to sleep between requests
	--debug               debug logging
	--log-file LOG_FILE   log file for output


`--reqs` can fire off as many parallel requests as applied (tested
upto 10k), session is reused, so if the keep_alive time out is
exceeded this may fail wierdly
