from django.db import models
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_text

def _html_field_name(original_field_name):
    return '_{}_html'.format(original_field_name)

class Pandoc(object):
    '''A Pandoc object to be used with the PandocField. It has 2 properties: ``raw`` and ``rendered``. ``raw`` returns the raw string, and ``html`` returns the rendered string.'''

    def __init__(self, raw_string):
        self.raw = raw_string

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
        return mark_safe(smart_text(self.rendered))

    __unicode__ = __str__

class PandocField(models.TextField):
    '''A model field that automatically updates the rendered HTML of a raw Pandoc string when the instance is saved.'''

    description = "An advanced Markdown field that supports LaTeX formulas"

    def __init__(self, *args, **kwargs):
        self.html_field = not kwargs.pop('html_field', False)
        super(PandocField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.html_field and not cls._meta.abstract:
            html_field = models.TextField(editable=False, blank=True)
            html_field.creation_counter = self.creation_counter + 1
            cls.add_to_class(_html_field_name(name), html_field)
        super(MarkupField, self).contribute_to_class(cls, name)

    def deconstruct(self):
        name, path, args, kwargs = super(MarkupField, self).deconstruct()
        kwargs['html_field'] = True
        return name, path, args, kwargs

    def pre_save(self, model_instance, add):
        value = super(PandocField, self).pre_save(model_instance, add)
        if value.raw is not None:
            # todo: provide a better conversion method :-)
            html = '<p>{}</p>'.format(value.raw)
        else:
            html = None
        setattr(model_instance, _html_field_name(self.attname), html)
        return value.raw
