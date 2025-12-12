from django import template
from women.models import Category, TagPost, Women
from django.db.models import Count
import women.views as views

register = template.Library()




# @register.simple_tag(name="get_menu")
# def get_menu():
#     return menu


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected=0):
    # cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    cats = Category.objects.filter(posts__is_published__gt=0).distinct()
    return {
        "cats": cats,
        "cat_selected": cat_selected
    }


@register.inclusion_tag("women/list_tags.html")
def show_all_tags(tag_selected=0):
    # tags = TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)
    tags = TagPost.objects.filter(tags__gt=0).distinct()
    return {
        "tags": tags,
        "tag_selected": tag_selected
    }
