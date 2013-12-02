from django.contrib import admin
from plumbaker.apps.category.models import Category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('slug', 'title')
	prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)