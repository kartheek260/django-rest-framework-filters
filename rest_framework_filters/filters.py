from __future__ import absolute_import
from __future__ import unicode_literals

from django.utils import six

from django_filters.rest_framework.filters import *
from rest_framework_filters.utils import import_class


ALL_LOOKUPS = '__all__'


class AutoFilter(Filter):
    def __init__(self, *args, **kwargs):
        self.lookups = kwargs.pop('lookups', [])

        super(AutoFilter, self).__init__(*args, **kwargs)


class RelatedFilter(AutoFilter, ModelChoiceFilter):
    def __init__(self, filterset, *args, **kwargs):
        self.filterset = filterset
        kwargs.setdefault('lookups', None)

        super(RelatedFilter, self).__init__(*args, **kwargs)

    def filterset():
        def fget(self):
            if isinstance(self._filterset, six.string_types):
                self._filterset = import_class(self._filterset)
            return self._filterset

        def fset(self, value):
            self._filterset = value

        return locals()
    filterset = property(**filterset())

    @property
    def field(self):
        # if no queryset is provided, default to the filterset's default queryset
        self.extra.setdefault('queryset', self.filterset._meta.model._default_manager.all())
        return super(RelatedFilter, self).field


class AllLookupsFilter(AutoFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookups', ALL_LOOKUPS)

        super(AllLookupsFilter, self).__init__(*args, **kwargs)
