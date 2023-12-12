from django.template.defaulttags import register


@register.filter(name='get')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(str(key))
