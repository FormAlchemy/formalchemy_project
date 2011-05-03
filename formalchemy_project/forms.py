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

# setting the autocomplete field
Widgets = FieldSet(models.Widgets)
Widgets.configure()
Widgets.autocomplete.set(renderer=jq.autocomplete(['%sanux' % s for s in 'BCDFGHJKLMNP']))

# don't wan't to show user in edit form
Article = FieldSet(models.Article)
Article.configure()
del Article.user

# User.group is not a many to many relation
User = FieldSet(models.User)
User.group.set(renderer=jq.relation())

# The Group form is used to view an instance in the admin UI
Group = FieldSet(models.Group)

# playing with tabs...
GroupTabs = jq.Tabs('tabs',
        ('users', 'Users', Group.copy('users')),
        ('permissions', 'Permissions', Group.copy('permissions')),
    )

# The GroupEdit form is used to edit an instance in the admin UI
GroupEdit = jq.MultiFieldSet('groups',
            ('name', '', Group.copy('name')),
            ('others', '', GroupTabs),
          )


## Initialize grids

