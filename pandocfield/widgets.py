from django import forms

class PandocEditor(forms.widgets.Textarea):
    """Form widget specifically for editing PandocFields

    """
    def render(self, name, value, attrs=None):
        if hasattr(value, 'raw'):
            value = value.raw
        return super(PandocEditor, self).render(name, value, attrs)
