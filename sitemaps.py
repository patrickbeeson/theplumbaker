from django.contrib.sitemaps import Sitemap
from plumbaker.apps.press.models import Release
from plumbaker.apps.inventory.models import Good
import datetime

class NewsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Release.live.all()

	def lastmod(self, obj):
		return obj.pub_date

	def location(self, obj):
		return "/press/%s" % obj.slug

class GoodsSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Good.objects.all()

	def location(self, obj):
		return "/baked-goods/%s" % obj.slug