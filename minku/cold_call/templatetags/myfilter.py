from django.template.defaulttags import register


@register.filter
def get_item(d, key_name):
    value = ""
    try:
        value = d[key_name]
    except KeyError:
        value = ""
    return value
