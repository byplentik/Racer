from django import template

from django.contrib.auth import get_user_model as User
from basket.models import Category


register = template.Library()


@register.inclusion_tag('tags_html/sidebar_tag.html')
def sidebar(request):
    if request.user.is_authenticated and request.path.startswith('/user/'):
        return {'request': request, 'auth_path': True}
    elif request.user.is_authenticated and request.path.startswith('/cart/'):
        return {'request': request, 'auth_path': True}
    return {'request': request, 'auth_path': False, 'categories': Category.objects.all()}


