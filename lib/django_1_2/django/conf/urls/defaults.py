from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import get_callable, RegexURLPattern, RegexURLResolver
from django.utils.importlib import import_module

__all__ = ['handler404', 'handler500', 'include', 'patterns', 'url']

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'

def _validate_urls(mod):
    while True:
        if isinstance(mod, basestring):
            mod = import_module(mod)
        elif isinstance(mod, tuple):
            mod = mod[0]
        elif isinstance(mod, list):
            break
        else:
            mod = mod.urlpatterns
    assert all(isinstance(p, (RegexURLPattern, RegexURLResolver)) for p in mod)

def include(arg, namespace=None, app_name=None):
    if isinstance(arg, tuple):
        # callable returning a namespace hint
        if namespace:
            raise ImproperlyConfigured('Cannot override the namespace for a dynamic module that provides a namespace')
        urlconf_module, app_name, namespace = arg
    else:
        _validate_urls(arg)
        # No namespace hint - use manually provided namespace
        urlconf_module = arg
    return (urlconf_module, app_name, namespace)

def patterns(prefix, *args):
    pattern_list = []
    for t in args:
        if isinstance(t, (list, tuple)):
            assert isinstance(t[0], basestring)
            if isinstance(t[1], tuple):
                _validate_urls(t[1])
            else:
                assert callable(t[1]) or get_callable('%s.%s' % (prefix, t[1]))
            t = url(prefix=prefix, *t)
        elif isinstance(t, RegexURLPattern):
            t.add_prefix(prefix)
        else:
            assert "Unrecognized URL pattern item %r" % t
        pattern_list.append(t)
    return pattern_list

def url(regex, view, kwargs=None, name=None, prefix=''):
    if isinstance(view, (list,tuple)):
        # For include(...) processing.
        urlconf_module, app_name, namespace = view
        return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
    else:
        if isinstance(view, basestring):
            if not view:
                raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
            if prefix:
                view = prefix + '.' + view
        return RegexURLPattern(regex, view, kwargs, name)

