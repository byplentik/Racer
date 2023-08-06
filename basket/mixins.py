from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class CreateSessionKeyMixin:
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.session.session_key is None:
            request.session['user'] = 'Anonymous user'
        return super().dispatch(request, *args, **kwargs)