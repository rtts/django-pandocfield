from django import forms
from django.template import Context, loader
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
        attrs['style'] = 'height: 15em; width: 690px'
        final_attrs = self.build_attrs(attrs, name=name)
        template = loader.get_template('pandocfield/widget.html')
        return template.render(Context({
            'attrs': flatatt(final_attrs),
            'value': force_text(value),
        }))
