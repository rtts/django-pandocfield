# Django Pandoc Field

***An advanced Markdown field for Django that supports LaTeX formulas***

## Introduction

Despite some excellent libraries ([django-pagedown](https://github.com/timmyomahony/django-pagedown), [django-markdown-deux](https://github.com/trentm/django-markdown-deux), [django-markupfield](https://github.com/jamesturk/django-markupfield)), there is currently no Django app that lets users supply [Markdown](http://daringfireball.net/projects/markdown/) with embedded [LaTeX formulas](https://en.wikibooks.org/wiki/LaTeX/Mathematics). For examples of advanced Markdown editors that do support this, check out [Markx](http://markx.herokuapp.com/), [StackEdit](https://stackedit.io/), or the editor used on [Mathematics Stack Exchange](http://math.stackexchange.com/). Python's own [markdown module](http://pythonhosted.org/Markdown/) bundles [a number of extensions](http://pythonhosted.org/Markdown/extensions/index.html#officially-supported-extensions), but unfortunately doesn't do math typesetting. Therefore, the goal of this project is to provide a Django field that accepts Markdown code interspersed with LaTeX formulas and renders it fast and safely to HTML.

### Pandoc

[Pandoc](http://pandoc.org/) is the world's best markdown converter: It is fast due to natively compiled code and it supports all possible extensions to Markdown syntax, including the typesetting of formulas using either [MathML](https://www.w3.org/TR/MathML3/), [MathJax](https://www.mathjax.org/), or [KaTeX](https://khan.github.io/KaTeX/) (among others). It is written in [Haskell](https://www.haskell.org/), the programming language of the gods, and is [easily extendable with Python code](http://pandoc.org/scripting.html). As the name implies, `django-pandocfield` uses Pandoc in the background to convert user-supplied Markdown to HTML for displaying on web pages.

To install Pandoc on Debian-derived systems, use the [Apt package manager](https://debian-handbook.info/browse/stable/sect.apt-get.html):

    # apt install pandoc

For other systems, refer to [Pandoc's installation instructions](http://pandoc.org/installing.html).

## Installation

Django Pandoc Field is not (yet!) installable via package managers such as `apt` or `pip`. Simply clone this repository and run `python setup.py install`. You can also copy the `pandocfield` directory into your own Django project.

## Configuration
First, add `pandocfield` to your `INSTALLED_APPS` (in `setup.py`):

    INSTALLED_APPS += ['pandocfield']

Second, add `pandocfield.PandocField()` to your desired model (in `models.py`):

    from django import models
    from pandocfield import PandocField

    class ScientificArticle(models.Model):
        content = PandocField()

Third, create and run the database migrations:

    $ ./manage.py makemigrations
    $ ./manage.py migrate

Finally, make sure to include the [MathJax javascript library](https://github.com/mathjax/MathJax) on each page that displays the contents of a PandocField:

    <script src="{% static 'mathjax/MathJax.js' %}?config=TeX-AMS-MML_HTMLorMML"></script>
