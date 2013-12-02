from django.db import models
from django.contrib.contenttypes import generic

from plumbaker.apps.media.models import Photo
from markdown import markdown
from plumbaker.apps.related_links.models import RelatedLink

class Ingredient(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(help_text='This field will prepopulate from the name field.', unique=True)
	description = models.TextField(help_text='A brief description of this ingredient. Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a>.', blank=True)
	description_html = models.TextField(editable=False, blank=True)
	lead_photo = models.ForeignKey(Photo, null=True, blank=True, help_text='Photo will be resized on the template.')
	keywords = models.CharField(max_length=200, blank=True, help_text='Enter a comma-separated list of keywords.')
	related_links = generic.GenericRelation(RelatedLink)
	
	class Meta:
		verbose_name_plural = 'ingredients'
		
	def __unicode__(self):
		return self.name

	def save(self):
		self.description_html = markdown(self.description)
		super(Ingredient, self).save()
	
	def get_absolute_url(self):
		return '/ingredients/%s/' % (self.slug)