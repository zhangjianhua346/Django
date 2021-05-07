from django.template import Library

register = Library()

@register.filter
def makedown(value):
    import markdown
    return markdown.markdown(value)