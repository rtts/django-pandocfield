from __future__ import unicode_literals
import inspect
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import python_2_unicode_compatible
from . import widgets
from .utils import pandoc

@python_2_unicode_compatible
class Pandoc(object):
    """A Pandoc object to be used with the PandocField

    It has 2 properties: ``raw`` and ``html``. ``raw`` returns the
    raw string, and ``html`` returns the rendered string. The __str__()
    method always returns the rendered string.

    """
    def __init__(self, raw_string, html_string):
        self._raw = raw_string
        self._html = html_string

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, val):
        self._raw = val

    @property
    def html(self):
        return self._html

    def __str__(self):
        return mark_safe(self._html)

class PandocField(models.TextField):
    """An advanced Markdown field that supports LaTeX formulas

    """
    def __init__(self, *args, **kwargs):
        if 'auto_create_html_field' in kwargs:
            self.auto_create_html_field = kwargs['auto_create_html_field']
            del kwargs['auto_create_html_field']
        else:
            self.auto_create_html_field = True
        super(PandocField, self).__init__(*args, **kwargs)

    def __get__(self, obj, cls):
        raw_value = obj.__dict__[self.name]
        html_value = obj.__dict__[self.html_field.name]
        return Pandoc(raw_value, html_value)

    def __set__(self, obj, value):
        if isinstance(value, Pandoc):
            obj.__dict__[self.name] = value.raw
            obj.__dict__[self.html_field.name] = value.html
        else:
            obj.__dict__[self.name] = value

    def contribute_to_class(self, cls, name):
        if self.auto_create_html_field and not cls._meta.abstract:
            self.html_field = models.TextField(editable=False, blank=True)
            self.html_field.creation_counter = self.creation_counter + 1
            cls.add_to_class('_{}_html'.format(name), self.html_field)
        super(PandocField, self).contribute_to_class(cls, name)
        setattr(cls, name, self)

    def deconstruct(self):
        name, path, args, kwargs = super(PandocField, self).deconstruct()
        kwargs['auto_create_html_field'] = False
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = super(PandocField, self).pre_save(model_instance, add)

        # This is where the actual conversion happens
        html = pandoc(value.raw)

        setattr(model_instance, self.html_field.name, html)
        return value.raw

    def get_prep_value(self, value):
        if isinstance(value, Pandoc):
            return value.raw
        else:
            return value

    def to_python(self, value):
        if isinstance(value, Pandoc):
            return value
        else:
            return super(PandocField, self).to_python(value)

    def formfield(self, **kwargs):
        defaults = {'widget': widgets.PandocEditor}
        defaults.update(kwargs)
        return super(PandocField, self).formfield(**defaults)

    # def value_to_string(self, obj):
    #     value = self.value_from_object(obj)
    #     raise ValueError(type(value))
    #     if hasattr(value, 'raw'):
    #         return value.raw
    #     return value

# Use the PandocEditorWidget in the Admin
from django.contrib.admin.options import FORMFIELD_FOR_DBFIELD_DEFAULTS
FORMFIELD_FOR_DBFIELD_DEFAULTS[PandocField] = {
    'widget': widgets.PandocEditor,
}
