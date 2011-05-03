# -*- coding: utf-8 -*-
from formalchemy_project import models
from formalchemy import config as fa_config
from formalchemy import templates
from formalchemy import validators
from formalchemy import fields
from formalchemy import forms
from formalchemy import tables
from formalchemy.ext.fsblob import FileFieldRenderer
from formalchemy.ext.fsblob import ImageFieldRenderer
import fa.jquery as jq

fa_config.encoding = 'utf-8'
fa_config.engine = jq.TemplateEngine()

## Use jquery renderers
forms.FieldSet.default_renderers.update(jq.default_renderers)
forms.FieldSet.default_renderers['dropdown'] = jq.relations()

class FieldSet(forms.FieldSet):
    pass

class Grid(tables.Grid):
    pass

## Initialize fieldsets

Widgets = FieldSet(models.Widgets)
Widgets.configure()
Widgets.autocomplete.set(renderer=jq.autocomplete(['%sanux' % s for s in 'BCDFGHJKLMNP']))

Article = FieldSet(models.Article)
Article.configure()
del Article.user
## Initialize grids

