from django import template

register = template.Library()

@register.simple_tag
def without_tax(price=150,perc=5):
    val = price * 1 / (1 + ( float(perc) / 100))
    return round(val,2)

@register.simple_tag
def tax(price,perc):
    val = price * 1 / (1 + ( float(perc) / 100))
    total = (price - val)
    return round(total,2)

@register.simple_tag
def divideby(val, divideby):
    value = val/divideby
    return round(value,2)

@register.simple_tag
def multiplyby(val, multiby):
    value = val * multiby
    return round(value, 2)

@register.simple_tag
def count_days(date1,date2):
    val = date1.day - date2.day
    return val