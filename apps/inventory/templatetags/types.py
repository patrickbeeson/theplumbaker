from django import template
from plumbaker.apps.inventory.models import Type

class GoodTypeListNode(template.Node):
	def __init__(self, varname):
		self.varname = varname
	
	def render(self, context):
		context[self.varname] = Type.objects.all()
		return ''

def do_get_goodtypes_list(parser, token):
	"""
	Gets a list of all types, and passes it into a custom variable.
	
	Syntax::
	
		{% get_goodtypes as [varname] %}
	
	Example::
	
		{% get_goodtypes as good_type_list %}
	"""
	bits = token.contents.split()
	if len(bits) != 3:
		raise template.TemplateSyntaxError, "'%s' tag takes two arguements" % bits[0]
	if bits[1] != "as":
		raise template.TemplateSyntaxError, "First arguement to '%s' tag must be 'as'" % bits[0]
	return GoodTypeListNode(bits[2])

register = template.Library()
register.tag('get_goodtypes_list', do_get_goodtypes_list)