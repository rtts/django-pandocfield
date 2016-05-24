from __future__ import unicode_literals
import inspect
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import python_2_unicode_compatible

def _html_field_name(original_field_name):
    return '_{}_html'.format(original_field_name)

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

class PandocDescriptor(object):
    """A descriptor that converts strings to Pandoc objects

    """
    def __init__(self, field):
        self.raw_field = field.name
        self.html_field = _html_field_name(field.name)

    def __get__(self, obj, cls):
        raw_value = obj.__dict__[self.raw_field]
        html_value = obj.__dict__[self.html_field]
        return Pandoc(raw_value, html_value)

    def __set__(self, obj, value):
        if isinstance(value, Pandoc):
            obj.__dict__[self.raw_field] = value.raw
            obj.__dict__[self.html_field] = value.html
        else:
            obj.__dict__[self.raw_field] = value

class PandocField(models.TextField):
    """An advanced Markdown field that supports LaTeX formulas

    """
    def __init__(self, *args, auto_create_html_field=True, **kwargs):
        self.auto_create_html_field = auto_create_html_field
        super(PandocField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.auto_create_html_field and not cls._meta.abstract:
            html_field = models.TextField(editable=False, blank=True)
            html_field.creation_counter = self.creation_counter + 1
            cls.add_to_class(_html_field_name(name), html_field)
        super(PandocField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, PandocDescriptor(self))

    def deconstruct(self):
        name, path, args, kwargs = super(PandocField, self).deconstruct()
        kwargs['auto_create_html_field'] = False
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = super(PandocField, self).pre_save(model_instance, add)

        # todo: provide a better conversion method :-)
        html = '<b>{}</b>'.format(value.raw)

        setattr(model_instance, _html_field_name(self.attname), html)
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

    # def value_to_string(self, obj):
    #     value = self.value_from_object(obj)
    #     raise ValueError(type(value))
    #     if hasattr(value, 'raw'):
    #         return value.raw
    #     return value
