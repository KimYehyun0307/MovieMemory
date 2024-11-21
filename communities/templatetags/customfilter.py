# communities/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """딕셔너리에서 key로 값을 가져오는 필터"""
    return dictionary.get(key)
