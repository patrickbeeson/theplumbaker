import os
import Image
from django import template

register = template.Library()

def thumbnail(file, size='104x104'):
	"""
	A filter to resize an ImageField on demand. Default is 104 by 104 pixels.
	
	Usage::
	
		<img src="{{ object.image.url }}" alt="original image"> 
		
		<img src="{{ object.image|thumbnail }}" alt="image resized to default 104x104 format"> 
		
		<img src="{{ object.image|thumbnail:200x300 }}" alt="image resized to 200x300">
	"""
	# defining the size
	x, y = [int(x) for x in size.split('x')]
	# defining the filename and the miniature filename
	filehead, filetail = os.path.split(file.path)
	basename, format = os.path.splitext(filetail)
	miniature = basename + '_' + size + format
	filename = file.path
	miniature_filename = os.path.join(filehead, miniature)
	filehead, filetail = os.path.split(file.url)
	miniature_url = filehead + '/' + miniature
	if os.path.exists(miniature_filename) and os.path.getmtime(filename)>os.path.getmtime(miniature_filename):
		os.unlink(miniature_filename)
	# if the image wasn't already resized, resize it
	if not os.path.exists(miniature_filename):
		image = Image.open(filename)
		image.thumbnail([x, y], Image.ANTIALIAS)
		try:
			image.save(miniature_filename, image.format, quality=90, optimize=1)
		except:
			image.save(miniature_filename, image.format, quality=90)

	return miniature_url

register.filter(thumbnail)