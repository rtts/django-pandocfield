from django import forms
from django.template import loader
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.encoding import force_text

class PandocEditor(forms.widgets.Textarea):
    """Form widget specifically for editing PandocFields

    """
    def render(self, name, value, attrs={}):
        if value is None:
            value = ''
        elif hasattr(value, 'raw'):
            value = value.raw
        attrs['style'] = 'font-family: monospace; line-height: 1.5; height: 25em; width: calc(100% - 190px) !important'
        final_attrs = self.build_attrs(attrs, name=name)
        template = loader.get_template('pandocfield/widget.html')
        return template.render({
            'attrs': flatatt(final_attrs),
            'value': force_text(value),
        })
