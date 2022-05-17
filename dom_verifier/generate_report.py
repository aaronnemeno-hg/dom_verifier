#!/usr/bin/python3

import os
import logging
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from dom_verifier.spiders.pages_spider import PagesSpider

load_dotenv()

SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

items = []
class ItemCollectorPipeline(object):

    def __init__(self):
        self._ids_seen = set()

    def process_item(self, item, spider):
        print("ITEM FOUND:")
        print(item)
        items.append(item)


def script_tag_has(item_has):
    if item_has == "1":
        return "yes"
    elif item_has == "0":
        return "no"
    return item_has

if __name__ == "__main__":
    process = CrawlerProcess({
        'ROBOTSTXT_OBEY': True,
        'LOG_LEVEL': 'INFO',
        'HTTPERROR_ALLOW_ALL': True,
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': .5, # 500ms delay
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': [
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/57.0.2987.110 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.79 '
             'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
             'Gecko/20100101 '
             'Firefox/55.0')  # firefox
        ]
    })
    process.crawl(PagesSpider)
    process.start()

    # generate datetime by timezone
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    pst_dt_report = pst_now.strftime("%Y-%m-%d")

    # print the items
    blocks = [{
        "type": "divider"
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Daily Analytics Script Tag Finder Report - {}"\
                    .format(pst_dt_report)
        }
    }]

    for item in items:

        print(dict(item));
        # generate block item section text
        bi_section_text = "\n∙ *url:* {}"\
                .format(item['url'])
        bi_section_text += "\n    ◦ response status code: *{}*"\
                .format(item['status_code'])

        has_src = script_tag_has(item['gt_src'])
        bi_section_text += "\n    ◦ has script tag with src: *{}*"\
                .format(has_src)

        has_code = script_tag_has(item['gt_code'])
        bi_section_text += "\n    ◦ has script tag with code: *{}*"\
                .format(has_code)

        block_item = {"type": "section", "text": {"type": "mrkdwn"}}
        print("url:", item['url'], "status_code:", item['status_code'])
        # update block item
        block_item['text'].update({'text': bi_section_text})

        blocks.append(block_item)

    #blocks = [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
    client = WebClient(token=SLACK_BOT_TOKEN)

    try:
        client.chat_postMessage(channel="#pixel-automation-test",
                 text='', blocks=blocks)
    except SlackApiError as e:
        print("ERROR SLACK", e.response['error'])


