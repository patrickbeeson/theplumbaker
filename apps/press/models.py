from django.db import models
from django.contrib.sitemaps import ping_google
from django.contrib.auth.models import User

import datetime
from markdown import markdown

from plumbaker.apps.media.models import Photo
from plumbaker.apps.category.models import Category

class Mention(models.Model):
	PUBLICATION_TYPES = (
		(u'NEWSPAPER', u'Newspaper'),
		(u'TELEVISION', u'Television'),
		(u'MAGAZINE', u'Magazine'),
		(u'WEBSITE', u'Web site'),
		(u'BLOG', u'Blog'),
		(u'TWITTER', u'Twitter'),
		(u'FACEBOOK', u'Facebook'),
		(u'OVERHEARD', u'Overheard'),
	)
	publication_name = models.CharField(max_length=200)
	publication_type = models.CharField(max_length=200, choices=PUBLICATION_TYPES)
	link = models.URLField(blank=True)
	pub_date = models.DateField()
	mention_title = models.CharField(max_length=500, blank=True, help_text='Use this field for a story headline.')
	mention_text = models.TextField(blank=True, help_text='Use this field for citing specific passages in the press mention, or for brief mentions such as Twitter or Facebook.')
	mention_text_html = models.TextField(editable=False, blank=True)
	keywords = models.CharField(max_length=200, blank=True, help_text='Enter a comma-separated list of keywords.')
	
	def save(self):
		self.mention_text_html = markdown(self.mention_text)
		super(Mention, self).save()

class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class Release(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date', help_text='This field will prepopulate from the headline.')
    headline = models.CharField(max_length=50)
    summary = models.TextField(help_text='Please use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown syntax</a> if needed.')
    summary_html = models.TextField(editable=False, blank=True)
    body = models.TextField(help_text='Please use the WYSIWYG for adding style elements instead of using HTML or CSS. Do not copy and paste from a text editor like Microsoft Word.')
    category = models.ForeignKey(Category)
    lead_photo = models.ForeignKey(Photo, null=True, blank=True, help_text='Photo will be resized on the template.')
    keywords = models.CharField(max_length=200, blank=True, help_text='Enter a comma-separated list of keywords.')
    description = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS, help_text='Only press releases with "Live" status will be displayed.')
    objects = models.Manager()
    live = LiveEntryManager()
        
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'release'
        verbose_name_plural = 'releases'
    
    def __unicode__(self):
        return self.headline

#    def save(self):
#        self.summary_html = markdown(self.summary)
#        super(Release, self).save()
#        try:
#        	ping_google()
#        except Exception:
#        	pass
    
    def get_absolute_url(self):
        return '/press/%s/%s/' % (self.pub_date.strftime('%Y/%b/%d').lower(), self.slug)   