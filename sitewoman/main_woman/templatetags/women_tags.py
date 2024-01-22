from django import template
from django.db.models import Count

import main_woman.views as views

from main_woman.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('main_woman/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0, posts__is_published=True)

    return {"cats": cats, "select": cat_selected}


@register.inclusion_tag('main_woman/list_tags.html')
def show_all_tags():

    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
