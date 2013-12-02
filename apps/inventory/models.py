from django.db import models
from markdown import markdown
from plumbaker.apps.ingredients.models import Ingredient
from plumbaker.apps.availability.models import Location
from plumbaker.apps.media.models import Photo

class Good(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(help_text='This field will prepopulate from the name field.', unique=True)
	description = models.TextField(help_text='A brief summary of this baked good. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	description_html = models.TextField(editable=False, blank=True)
	good_type = models.ForeignKey('Type')
	ingredients = models.ManyToManyField(Ingredient)
	lead_photo = models.ForeignKey(Photo, null=True, blank=True, help_text='Photo will be resized on the template.')
	where_to_buy = models.ManyToManyField(Location, blank=True)
	is_seasonal = models.BooleanField(default=False)
	is_available = models.BooleanField(default=True)
	keywords = models.CharField(max_length=200, blank=True, help_text='Enter a comma-separated list of keywords.')
	google_checkout_html = models.TextField(blank=True)
	google_checkout_javascript = models.TextField(blank=True)

	class Meta:
		verbose_name_plural = 'goods'
		
	def __unicode__(self):
		return self.name

	def save(self):
		self.description_html = markdown(self.description)
		super(Good, self).save()
	
	def get_absolute_url(self):
		return '/baked-goods/%s/' % (self.slug)

class Portion(models.Model):
	PORTION_TYPES = (
		(u'S', u'Small'),
		(u'M', u'Medium'),
		(u'L', u'Large'),
		(u'PL', u'Petite loaf'),
		(u'FL', u'Full loaf'),
	)
	portion_type = models.CharField(max_length=2, choices=PORTION_TYPES)
	quantity = models.PositiveIntegerField()
	baked_good = models.ForeignKey(Good)
	cost = models.DecimalField(max_digits=5, decimal_places=2)
	nutritional_information = models.TextField(blank=True, help_text='The nutritional information for this portion size. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	nutritional_information_html = models.TextField(editable=False, blank=True)
	notes = models.TextField(help_text='Add any notes for this portion here. This will not be shown to the public.', blank=True)

	def save(self):
		self.nutritional_information_html = markdown(self.nutritional_information)
		super(Portion, self).save()

class Type(models.Model):
	title = models.CharField(max_length=50)
	slug = models.SlugField(help_text='This field will prepopulate from the title field.', unique=True)
	description = models.TextField(help_text='A brief description of this baked good type. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.')
	description_html = models.TextField(editable=False, blank=True)
	keywords = models.CharField(max_length=200, help_text='Comma-separated keywords describing the type. Limit 200 characters.', blank=True)
		
	class Meta:
		verbose_name_plural = 'types'
		
	def __unicode__(self):
		return self.title

	def save(self):
		self.description_html = markdown(self.description)
		super(Type, self).save()
	
	def get_absolute_url(self):
		return '/baked-good-types/%s/' % (self.slug)