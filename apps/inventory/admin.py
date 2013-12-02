from django.contrib import admin
from plumbaker.apps.inventory.models import Good, Portion, Type

class PortionInline(admin.TabularInline):
    model = Portion
    extra = 3
    fields = ('portion_type', 'quantity', 'cost', 'nutritional_information', 'notes')

class GoodAdmin(admin.ModelAdmin):
	list_display = ('slug', 'name', 'good_type','is_available',)
	list_filter = ('good_type', 'is_available',)
	search_fields = ('name', 'description',)
	prepopulated_fields = {'slug': ('name',)}
	fieldsets = [
		(None, {'fields': ('slug', 'name', 'description', 'lead_photo', 'good_type', 'ingredients', 'where_to_buy', 'is_seasonal', 'is_available',),}),
		('Meta options for SEO', {'fields': ('keywords',), 'classes': ('collapse',)}),
		('Google Checkout options', {'fields': ('google_checkout_html', 'google_checkout_javascript',), 'classes': ('collapse',)}),
	]
	inlines = [PortionInline]

admin.site.register(Good, GoodAdmin)

class TypeAdmin(admin.ModelAdmin):
	list_display = ('slug', 'title',)
	prepopulated_fields = {'slug': ('title',)}
	fieldsets = [
		(None, {'fields': ('title', 'slug', 'description',),}),
		('Meta options for SEO', {'fields': ('keywords',), 'classes': ('collapse',)}),
	]

admin.site.register(Type, TypeAdmin)