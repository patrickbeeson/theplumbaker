from django.contrib import admin
from plumbaker.apps.related_links.admin import RelatedLinkInline
from plumbaker.apps.ingredients.models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
	inlines = [
		RelatedLinkInline,
	]
	prepopulated_fields = { 'slug': ['name'] }
	fieldsets = [
		(None, {'fields': ('name', 'slug', 'description', 'lead_photo',),}),
		('Meta options for SEO', {'fields': ('keywords',), 'classes': ('collapse',)}),
	]

admin.site.register(Ingredient, IngredientAdmin)