from django import template
import random

register = template.Library()

def number_format(value):
    try:
        value = int(value)  
        if value >= 10000000:  
            return f"{value / 10000000:.2f} Crore"
        elif value >= 100000:  
            return f"{value / 100000:.2f} Lakh"
        elif value >= 1000:  
            return f"{value / 1000:.2f} Thousand"
        else:  
            return str(value)
    except (ValueError, TypeError):
        return value  

register.filter("number_format", number_format)

def size_format(value):
    try:
        value = int(float(value)) 
        value_str = f"{value:,}"  
        return value_str
    except (ValueError, TypeError):
        return value  

register.filter("size_format", size_format)

@register.filter
def unslug(value):
    return value.replace("-", " ").replace("_", " ").title()

@register.simple_tag
def random_number(min_value, max_value):
    return random.randint(min_value, max_value)