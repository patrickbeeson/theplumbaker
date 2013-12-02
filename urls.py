from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from django.contrib.sitemaps import FlatPageSitemap

from plumbaker.apps.availability.models import Location
from plumbaker.apps.inventory.models import Good, Portion, Type
from plumbaker.apps.ingredients.models import Ingredient
from plumbaker.apps.media.models import Photo
from plumbaker.apps.press.models import Mention, Release
from plumbaker.apps.category.models import Category
from plumbaker.feeds import LatestNewsFeed
from plumbaker.sitemaps import NewsSitemap, GoodsSitemap
from plumbaker.robots import robots_txt

admin.autodiscover()

# Category dicts
category_list_info_dict = {
	'queryset': Category.objects.all(),
	'allow_empty': True,
}

category_detail_info_dict = {
	'queryset': Category.objects.all(),
#	'extra_context' : {'release_list': get_live_releases},
	'template_object_name': 'category',
}

# Ingredient dicts
ingredient_list_info_dict = {
	'queryset': Ingredient.objects.all(),
	'allow_empty': True,
}

ingredient_detail_info_dict = {
	'queryset': Ingredient.objects.all(),
	'template_object_name': 'ingredient',
}

# Baked-good dicts
inventory_list_info_dict = {
	'queryset': Good.objects.all(),
	'allow_empty': True,
}

inventory_detail_info_dict = {
	'queryset': Good.objects.all(),
	'template_object_name': 'good',
}

# Location dicts
location_list_info_dict = {
	'queryset': Location.current.all(),
	'allow_empty': True,
}

location_detail_info_dict = {
	'queryset': Location.objects.all(),
	'template_object_name': 'location',
}

# Baked good types dicts
type_list_info_dict = {
	'queryset': Type.objects.all(),
	'allow_empty': True,
}

type_detail_info_dict = {
	'queryset': Type.objects.all(),
	'template_object_name': 'type',
}

# News dict
news_info_dict = {
	'queryset': Release.live.all(),
	'date_field': 'pub_date',
	'template_object_name': 'release',
}

news_list_info_dict = {
	'queryset': Release.live.all().order_by('-pub_date'),
	'paginate_by': 15,
}

# Mention dict
mention_list_info_dict = {
	'queryset': Mention.objects.all(),
	'allow_empty': True,
	'template_object_name': 'mention',
}

# Feeds
feeds = {
	'news': LatestNewsFeed,
}

# Sitemaps
sitemaps = {
	'news': NewsSitemap,
	'goods': GoodsSitemap,
    'flatpages': FlatPageSitemap,
}


urlpatterns = patterns('',
	# Robots
	(r'^robots.txt$', robots_txt),

	# Home page
	(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
	#(r'^$', 'patrickbeeson.views.home_page'),

	# Baked goods
	(r'^baked-goods/$', list_detail.object_list, inventory_list_info_dict),
	(r'^baked-goods/(?P<slug>[-\w]+)/$', list_detail.object_detail, inventory_detail_info_dict),

	# Baked good types
	(r'^baked-good-types/$', list_detail.object_list, type_list_info_dict),
	(r'^baked-good-types/(?P<slug>[-\w]+)/$', list_detail.object_detail, type_detail_info_dict),

	# Ingredients
	(r'^ingredients/$', list_detail.object_list, ingredient_list_info_dict),
	(r'^ingredients/(?P<slug>[-\w]+)/$', list_detail.object_detail, ingredient_detail_info_dict),

	# Category
	(r'^categories/$', list_detail.object_list, category_list_info_dict),
	(r'^categories/(?P<slug>[-\w]+)/$', list_detail.object_detail, category_detail_info_dict),

	# Locations
	(r'^locations/$', list_detail.object_list, location_list_info_dict),
	(r'^locations/(?P<slug>[-\w]+)/$', list_detail.object_detail, location_detail_info_dict),

	# News
	(r'^press/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', date_based.object_detail, dict(news_info_dict, slug_field='slug')),
	(r'^press/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', date_based.archive_day, news_info_dict),
	(r'^press/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', date_based.archive_month, news_info_dict),
	(r'^press/(?P<year>\d{4})/$', date_based.archive_year, dict(news_info_dict, make_object_list=True)),
	(r'^press/$', list_detail.object_list, news_list_info_dict),
	(r'^press/mentions/$', list_detail.object_list, mention_list_info_dict),

	# Contact form
	(r'^contact/', include('contact_form.urls')),
	
	# Feeds
	(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', { 'feed_dict': feeds }),
	
	# Sitemaps
	(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
	(r'^sitemap-(?P<section>.+).xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	
	# Flatpages
	(r'', include('django.contrib.flatpages.urls')),

)
