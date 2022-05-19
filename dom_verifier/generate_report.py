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

HYLINK_SITE_VERIFY = {
    # LOCAL
    # 'http://uclacn.local':{
        # 'require_ga': False,
        # 'require_gtm': False
    # },
    # 'http://magogallery.local':{
        # 'require_ga': False,
        # 'require_gtm': False
    # },
    ## PRODUCTION
    'https://hylinkdore.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://hylinktravel.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://hylinkventures.com/':{
        'require_ga': True,
        'require_gtm': False
    },
    'https://hylinkquantum.com/':{
        'require_ga': True,
        'require_gtm': False
    },
    'https://hylinkhelix.com/':{
        'require_ga': True,
        'require_gtm': False
    },
    'https://magogalleryglobal.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://oneleggedpigeon.com/':{
        'require_ga': True,
        'require_gtm': False
    },
    'https://hylinkpublicrelations.com/':{
        'require_ga': True,
        'require_gtm': False
    },
    'https://mena.uclahealth.org/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://culturelle.co.kr/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://culturelle.jp/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://sg.nanboya.global/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://hk.nanboya.global/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://culturelle.sg/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://cn.uclahealth.org/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://shyn.com/?fts=0&preview_theme_id=120649089124':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-dore.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-travel.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-ventures.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-hylinkquantum.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-helix.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-mago.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://staging-olp.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-publicrelations.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://newstaging-uclahealth.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://staging-culturellekr-wp.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://staging-culturellejp-wp.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://staging-culturellesg-wp.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://naboya-sg-staging.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://naboya-hk-staging.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://uclacn-stg.hylinkgroup.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://dmp-staging.hylinkgroup.com/home':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://esteelaudercampaignpage.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://esteelaudercelebrate.com/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://campaign.travelbeautifully.cn/staging/edmp_390/power/cdf_replenishment/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://wasabi.elcapps.com/appstartup_sanya/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/appstartup_haikou':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/apphomepageslideshow_sanya':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/apphomepageslideshow_haikou':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://wasabi.elcapps.com/appflighthomepage_sanya/':{
        'require_ga': False,
        'require_gtm': False
    },
    'https://wasabi.elcapps.com/appflighthomepage_haikou/':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/apphomepagefeed_sanya':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/appmembercenterpage_sanya':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/apphomepagefeed_haikou':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/appvacationhomepage_sanya':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://wasabi.elcapps.com/appvacationhomepage_haikou':{
        'require_ga': False,
        'require_gtm': False
    },
    'http://replenishment.elcapps.com/':{
        'require_ga': False,
        'require_gtm': False
    },
}

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
        return True, "yes"
    elif item_has == "0":
        return False, "no"
    return None, "N/A"

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

        try:
            ga_required = HYLINK_SITE_VERIFY[item['url']]['require_ga']

            # temporarily going to leave gtm aside as it's not required
            # as per this sheet: https://docs.google.com/spreadsheets/d/1vds3C2Sl-QfMKsqqm2zrPU1ohL_CqAcZROhsRFgCp-c/edit#gid=0
            gtm_required = HYLINK_SITE_VERIFY[item['url']]['require_gtm']
        except KeyError:
            ga_required, gtm_required = False, False

        # generate block item section text
        bi_section_text = "\n∙ *url:* {}"\
                .format(item['url'])
        bi_section_text += "\n    ◦ response status code: *{}*"\
                .format(item['status_code'])

        has_src, _ = script_tag_has(item['gt_src'])
        #bi_section_text += "\n    ◦ has script tag with src: *{}*"\
        #        .format(_)

        has_code, _ = script_tag_has(item['gt_code'])
        bi_section_text += "\n    ◦ has script tag with code: *{}*"\
                .format(_)

        block_item = {"type": "section", "text": {"type": "mrkdwn"}}
        print("url:", item['url'], "status_code:", item['status_code'])

        # update block item
        block_item['text'].update({'text': bi_section_text})

        if ga_required and not has_code:
            # google analytics is required and has no script with code
            blocks.append(block_item)

    # if blocks length == 2, this means all sites have passed the
    # google tag manager / google analytics check check
    if len(blocks) == 2:
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "∙ All supported sites have google tag manager / google analytics script tag."
            }
        });

    try:
        client = WebClient(token=SLACK_BOT_TOKEN)
        client.chat_postMessage(channel="#pixel-automation-test",
                 text='', blocks=blocks)
    except SlackApiError as e:
        print("ERROR SLACK", e.response['error'])


