from django.db import models
from django.contrib.localflavor.us.models import *
from django.contrib.contenttypes import generic

from markdown import markdown
from plumbaker.apps.media.models import Photo
from plumbaker.apps.related_links.models import RelatedLink

class CurrentVendorManager(models.Manager):
    def get_query_set(self):
        return super(CurrentVendorManager, self).get_query_set().filter(is_current_vendor=True)

class Location(models.Model):
	LOCATION_TYPES = (
		(u'W', u'Web site'),
		(u'S', u'Store'),
		(u'MT', u'Market'),
		(u'CS', u'Coffee shop'),
	)
	name = models.CharField(max_length=50)
	slug = models.SlugField(help_text='This field will prepopulate from the name field.', unique=True)
	location_type = models.CharField(max_length=2, choices=LOCATION_TYPES)
	description = models.TextField(help_text='A brief description of this location. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	description_html = models.TextField(editable=False, blank=True)
	street_address = models.CharField(max_length=200)
	city = models.CharField(max_length=200)
	zip_code = models.IntegerField()
	state = USStateField()
	latitude = models.DecimalField(blank=True, help_text="Use for map display.", max_digits=20, decimal_places=10)
	longitude = models.DecimalField(blank=True, help_text="Use for map display.", max_digits=20, decimal_places=10)
	phone_number = PhoneNumberField(blank=True)
	web_site = models.URLField(blank=True)
	email_address = models.EmailField(blank=True)
	lead_photo = models.ForeignKey(Photo, null=True, blank=True, help_text='Photo will be resized on the template.')
	keywords = models.CharField(max_length=200, blank=True, help_text='Enter a comma-separated list of keywords.')
	related_links = generic.GenericRelation(RelatedLink)
	is_current_vendor = models.BooleanField(default=True)
	objects = models.Manager()
	current = CurrentVendorManager()

	
	class Meta:
		verbose_name_plural = 'locations'
		
	def __unicode__(self):
		return self.name

	def save(self):
		self.description_html = markdown(self.description)
		super(Location, self).save()
	
	def get_absolute_url(self):
		return '/locations/%s/' % (self.slug)