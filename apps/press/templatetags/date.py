from django import template
from plumbaker.apps.press.models import Release

class ReleaseYearListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Release.live.dates("pub_date", "year")
		return ''

def do_get_release_year_list(parser, token):
	"""
	Gets a list of years in which releases are published.
	
	Syntax::
	
		{% get_release_year_list as [varname] %}
		
	Example::
	
		{% get_release_year_list as year_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return ReleaseYearListNode(bits[2])

class ReleaseMonthListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Release.live.dates("pub_date", "month")
		return ''

def do_get_release_month_list(parser, token):
	"""
	Gets a list of months in which releases are published.
	
	Syntax::
	
		{% get_release_month_list as [varname] %}
		
	Example::
	
		{% get_release_month_list as month_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return ReleaseMonthListNode(bits[2])
	
register = template.Library()
register.tag('get_release_month_list', do_get_release_month_list)
register.tag('get_release_year_list', do_get_release_year_list)