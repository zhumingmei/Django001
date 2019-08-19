from django import template
register = template.Library()

@register.inclusion_tag('page.html')
def page(num):
    return {'num':range(1,num + 1)}
