# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = 'xoxb-2093185909651-3525265464770-U5TlgnoHeppwmQGrPVM6b4oa'


class PagePipeline:
    def open_spider(self, spider):
        self.client = WebClient(token=SLACK_BOT_TOKEN)
        #self.file = open('result.json', 'w')

    def close_spider(self, spider):
        #self.file.close()
        pass

    def process_item(self, item, spider):
        try:
            self.client.chat_postMessage(channel="#pixel-automation-test",
                     text="Hello from your app :tada: ```{0}```"\
                             .format(json.dumps(dict(item))));
            return item
        except SlackApiError:
            print("ERROR SLACK", e.response['error'])

        #line = json.dumps(dict(item)) + "\n"
        #self.file.write(line)
