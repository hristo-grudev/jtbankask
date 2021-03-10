import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import JtbankaskItem
from itemloaders.processors import TakeFirst


class JtbankaskSpider(scrapy.Spider):
	name = 'jtbankask'
	start_urls = ['https://www.jtbanka.sk/o-banke/tlacove-spravy/']

	def parse(self, response):
		post_links = response.xpath('//h3[@class="press__title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="container relative"]//text()[normalize-space() and not(ancestor::nav |ancestor::a | ancestor::h1 | ancestor::p[contains(@class, "date")])]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[contains(@class, "date")]//text()[normalize-space()]').getall()
		date = [p.strip() for p in date]
		date = ' '.join(date).strip()

		item = ItemLoader(item=JtbankaskItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
