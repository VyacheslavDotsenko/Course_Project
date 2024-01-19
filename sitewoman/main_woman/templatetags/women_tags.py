from django import template
import main_woman.views as views

from main_woman.models import Category, TagPost

register = template.Library()


@register.inclusion_tag('main_woman/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()

    return {"cats": cats, "select": cat_selected}


@register.inclusion_tag('main_woman/list_tags.html')
def show_all_tags():

    return {"tags": TagPost.objects.all()}
