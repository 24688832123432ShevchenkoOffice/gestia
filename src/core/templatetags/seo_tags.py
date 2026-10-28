from django import template

from src.core.seo import DESCRIPTION_MAX, TITLE_MAX, clip_text, og_image_url
from src.core.seo_ld import build_graph, json_ld_script

register = template.Library()


@register.filter
def clip_title(value):
    return clip_text(value, TITLE_MAX)


@register.filter
def clip_description(value):
    return clip_text(value, DESCRIPTION_MAX)


@register.simple_tag(takes_context=True)
def og_image(context):
    return og_image_url(context)


@register.simple_tag(takes_context=True)
def structured_data(context):
    return json_ld_script(build_graph(context))
