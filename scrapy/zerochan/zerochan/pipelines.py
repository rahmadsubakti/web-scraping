# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ZerochanPipeline(object):
    def process_item(self, item, spider):
        return item

import os
from urllib.parse import urlparse

from scrapy.pipelines.images import ImagesPipeline

class CustomImagesPipeline(ImagesPipeline):
	def file_path(self, request, response=None, info=None):
		image_guid = os.path.basename(urlparse(request.url).path)
		return 'full/%s' % (image_guid)