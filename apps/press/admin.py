from django.contrib import admin
from plumbaker.apps.press.models import Release, Mention

class ReleaseAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('headline',)}
	list_display = ('headline', 'slug', 'pub_date')
	list_filter = ('status', 'pub_date', 'category')
	search_fields = ('headline', 'meta_description', 'summary', 'keywords')
	fieldsets = [
		(None, {'fields': ('author', 'pub_date', 'slug', 'headline', 'summary', 'body', 'lead_photo', 'category', 'status'),}),
		('Meta options for SEO', {'fields': ('keywords', 'description'), 'classes': ('collapse',)}),
	]
	raw_id_fields = ('lead_photo',)

admin.site.register(Release, ReleaseAdmin)

class MentionAdmin(admin.ModelAdmin):
	list_display = ('mention_title', 'publication_name', 'pub_date')
	list_filter = ('pub_date', 'publication_type',)
	search_fields = ('mention_title', 'publication_name', 'mention_text', 'publication_name',)
	fieldsets = [
		(None, {'fields': ('pub_date', 'publication_name', 'publication_type', 'mention_title', 'mention_text', 'link',),}),
		('Meta options for SEO', {'fields': ('keywords',), 'classes': ('collapse',)}),
	]

admin.site.register(Mention, MentionAdmin)