# DOM VERIFIER
###### Python script using Scrapy library to verify if google tag is installed on a list of sites supported by Hylink

## How To Install
- Follow the following commands below once done cloning the repository
```
cd dom_verifier/
virtualenv -p /usr/bin/python3.X venv
source venv/bin/activate
pip install -r requirements.txt
```

### Make sure that the following libraries are installed.
- Scrapy
- Scrapy User-Agent
- pytz
- Slack SDK

*If pip install requirements.txt didnt work please install manually.*
```
pip install pytz
pip install scrapy
pip install scrapy-useragents
pip install slack_sd
```

## Once libraries are installed go to target Spider file
```
cd dom_verifier/dom_verifier/spiders/pages_spider.py
```

- Comment out lines 17~18 (under For LOCAL TESTING)
- Uncomment out lines 22~71 (under For PRODUCTION)
