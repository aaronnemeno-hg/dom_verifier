# Built In
import time
import logging
logging.basicConfig(level=logging.DEBUG)

# Third Party
import scrapy
from scrapy.selector import Selector

# App
from dom_verifier.items import PageItem

class PagesSpider(scrapy.Spider):
    name = "pages"

    start_urls = [
        ## FOR LOCAL TESTING ##
        'http://uclacn.local',
        'http://magogallery.local',

        # For PRODUCTION
        # 'https://hylinkdore.com/',
        # 'https://hylinkgroup.com/',
        # 'https://hylinktravel.com/',
        # 'https://hylinkventures.com/',
        # 'https://hylinkquantum.com/',
        # 'https://hylinkhelix.com/',
        # 'https://magogalleryglobal.com/',
        # 'https://oneleggedpigeon.com/',
        # 'https://hylinkpublicrelations.com/',
        # 'https://mena.uclahealth.org/',
        # 'https://culturelle.co.kr/',
        # 'https://culturelle.jp/',
        # 'https://sg.nanboya.global/',
        # 'https://hk.nanboya.global/',
        # 'https://culturelle.sg/',
        # 'http://cn.uclahealth.org/',
        # 'https://shyn.com/?fts=0&preview_theme_id=120649089124',
        # 'https://newstaging-dore.hylinkgroup.com/',
        # 'https://newstaging.hylinkgroup.com/',
        # 'https://newstaging-travel.hylinkgroup.com/',
        # 'https://newstaging-ventures.hylinkgroup.com/',
        # 'https://newstaging-hylinkquantum.hylinkgroup.com/',
        # 'https://newstaging-helix.hylinkgroup.com/',
        # 'https://newstaging-mago.hylinkgroup.com/',
        # 'https://staging-olp.hylinkgroup.com/',
        # 'https://newstaging-publicrelations.hylinkgroup.com/',
        # 'https://newstaging-uclahealth.hylinkgroup.com/',
        # 'https://staging-culturellekr-wp.hylinkgroup.com/',
        # 'https://staging-culturellejp-wp.hylinkgroup.com/',
        # 'https://staging-culturellesg-wp.hylinkgroup.com/',
        # 'http://naboya-sg-staging.hylinkgroup.com/',
        # 'http://naboya-hk-staging.hylinkgroup.com/',
        # 'http://uclacn-stg.hylinkgroup.com/',
        # 'https://dmp-staging.hylinkgroup.com/home',
        # 'http://esteelaudercampaignpage.com/',
        # 'http://esteelaudercelebrate.com/',
        # 'http://campaign.travelbeautifully.cn/staging/edmp_390/power/cdf_replenishment/',
        # 'https://wasabi.elcapps.com/appstartup_sanya/',
        # 'http://wasabi.elcapps.com/appstartup_haikou',
        # 'http://wasabi.elcapps.com/apphomepageslideshow_sanya',
        # 'http://wasabi.elcapps.com/apphomepageslideshow_haikou',
        # 'https://wasabi.elcapps.com/appflighthomepage_sanya/',
        # 'https://wasabi.elcapps.com/appflighthomepage_haikou/',
        # 'http://wasabi.elcapps.com/apphomepagefeed_sanya',
        # 'http://wasabi.elcapps.com/appmembercenterpage_sanya',
        # 'http://wasabi.elcapps.com/apphomepagefeed_haikou',
        # 'http://wasabi.elcapps.com/appvacationhomepage_sanya',
        # 'http://wasabi.elcapps.com/appvacationhomepage_haikou',
        # 'http://replenishment.elcapps.com/',
        # 'https://lamer-dxb.com/'
        # 'http://jmllnycampaign.elcapps.com/',
        # 'http://elsupremepost.elcapps.com/index.html',
        # 'http://tfsatinmattereplenishment.elcapps.com/',
 ]

    def parse(self, response):
        print("USER AGENT REQUEST")
        print(response.request.headers['User-Agent'])
        item = PageItem()
        item['url'] = response.url

        item['status_code'] = response.status

        print("RESPONSE")
        print(dir(response))
        print("RESPONSE STATUS", response.status)
        print("RESPONSE STATUS TYPE", type(response.status))

        if response.status != 200:
            print("Response status not 200. Stopping process.")
            item['gt_src'] = 'N/A'
            item['gt_code'] = 'N/A'
            item['pixel_src'] = 'N/A'
            item['pixel_code'] = 'N/A'
        else:
            sel = Selector(response)
            # check if script contains code with 'gtm.js'
            xpath_query = '//script[contains(., "googletagmanager.com/gtm.js")]'
            gt_src_sel_gtm = sel.xpath(xpath_query)
            print("google tag code")
            print(gt_src_sel_gtm)

            # if not, do another check if it contains 'dataLayer.push'
            xpath_query = '//script[contains(., "dataLayer")]'
            gt_src_sel_dl = sel.xpath(xpath_query)
            print("google tag code - dataLayer")
            print(gt_src_sel_dl)

            if not gt_src_sel_gtm and not gt_src_sel_dl:
                item['gt_code'] = '0'
            else:
                item['gt_code'] = '1'

            xpath_query = '//script[contains(@src, "googletagmanager.com")]'
            gt_code_sel = sel.xpath(xpath_query)
            print("google tag src")
            print(gt_code_sel)
            if not gt_code_sel:
                item['gt_src'] = '0'
            else:
                item['gt_src'] = '1'

           # check if script contains code with 'gtm.js'
            xpath_query = '//script[contains(@src, "up_loader.1.1.0.js")]'
            pixel_src_sel = sel.xpath(xpath_query)
            print("pixel tag src")
            print(pixel_src_sel)
            if not pixel_src_sel:
                item['pixel_src'] = '0'
            else:
                item['pixel_src'] = '1'

            # if not, do another check if it contains 'dataLayer.push'
            xpath_query = '//script[contains(., "universalPixelApi.init")]'
            pixel_code_sel = sel.xpath(xpath_query)
            print("pixel tag code - universalPixelApi.init")
            print(pixel_code_sel)
            if not pixel_code_sel:
                item['pixel_code'] = '0'
            else:
                item['pixel_code'] = '1'

        yield item

