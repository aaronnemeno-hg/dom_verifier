# DOM VERIFIER
###### Python script using Scrapy library to verify if google tag is installed on a list of sites supported by Hylink

## How To Install
- Follow the following commands below once done cloning the repository
```
cd /home/<user>/<path_to_project>
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
pip install python-dotenv
pip install pytz
pip install scrapy
pip install scrapy-useragents
pip install slack_sdk
```

### Once libraries are installed go to target Spider file
```
cd home/<user>/<path_to_project>/dom_verifier/spiders/
vi pages_spider.py
```

### Do the following on vim mode
- Comment out lines 17~18 (under For LOCAL TESTING)
- Uncomment out lines 22~71 (under For PRODUCTION)

### Also create a `.env` file
```
cd home/<user>/<path_to_project>
vi .env
```

### Add the `SLACK_BOT_TOKEN` environment variable and its value
```
SLACK_BOT_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXX'
```

### After leaving the links for Script Tag checking, try to test the command below.
### You are going to append the command to cron.
```
/home/<user>/<path_to_project>/venv/bin/python /home/<user>/<path_to_project>/dom_verifier/generate_report.py
```
