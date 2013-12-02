from django.contrib import admin
from plumbaker.apps.availability.models import Location
from plumbaker.apps.related_links.admin import RelatedLinkInline

class LocationAdmin(admin.ModelAdmin):
	inlines = [
		RelatedLinkInline,
	]
	list_display = ('slug', 'name', 'location_type', 'is_current_vendor')
	fieldsets = [
		(None, {'fields': ('name', 'slug', 'is_current_vendor', 'location_type', 'description', 'lead_photo',),}),
		('Geo information', {'fields': ('street_address', 'city', 'zip_code', 'state', 'latitude', 'longitude',),}),
		('Contact information', {'fields': ('phone_number', 'web_site', 'email_address',),}),
		('Meta options for SEO', {'fields': ('keywords',), 'classes': ('collapse',)}),
	]
	prepopulated_fields = {'slug': ('name',)}

admin.site.register(Location, LocationAdmin)