from django.contrib.contenttypes import generic
from plumbaker.apps.related_links.models import RelatedLink


class RelatedLinkInline(generic.GenericStackedInline):
    extra = 3
    model = RelatedLink