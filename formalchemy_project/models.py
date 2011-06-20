"""The application's model objects"""
import transaction
import logging

from formalchemy import Column

from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relation
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from fa.jquery.utils import HTML, Color, Slider
from datetime import datetime

from pyramid_formalchemy import actions
from pyramid_formalchemy import renderers

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('formalchemy_project')

class Article(Base):
    __label__ = _('Article')
    __plural__ = _('Articles')
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, label=_('Id'))
    title = Column(Unicode, nullable=False, label=_('Title'))
    text = Column(HTML, label=_('Text'))
    publication_date = Column(Date, default=datetime.now, label=_('Publication date'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relation('User')


class Widgets(Base):
    __label__ = _('Widget')
    __plural__ = _('Widgets')
    __tablename__ = 'widgets'

    id = Column(Integer, primary_key=True)
    autocomplete = Column(Unicode, label=_('Auto complete'))
    slider = Column(Slider, default=0, label=_('Slider'))
    color = Column(Color, label=_('Color'))
    date = Column(Date, label=_('Date'))
    date_time = Column(DateTime, default=datetime.now, label=_('Date and time'))


class User(Base):
    __label__ = _('User')       # label used in UI
    __plural__ = _('Users')     # plural used in UI
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, label=_('Name')) # label is used in forms

    # the renderer argument will be used for the group relation. You can use a
    # backref_renderer option to set the renderer of the users relation
    group_id = Column(Integer, ForeignKey('groups.id'),
                      renderer=renderers.PyramidAutocompleteFieldRenderer(filter_by='name'))

    group = relation("Group", uselist=False, backref='users')

    def __unicode__(self):
        return self.name

group_permissions = Table('group_permissions', Base.metadata,
        Column('permission_id', Integer, ForeignKey('permissions.id')),
        Column('group_id', Integer, ForeignKey('groups.id')),
    )

class Group(Base):
    __label__ = _('Group')
    __plural__ = _('Groups')
    __tablename__ = 'groups'

    edit_buttons = actions.Actions('pyramid_formalchemy.actions.save', 'pyramid_formalchemy.actions.cancel')

    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, label=_('Name'))
    permissions = relation("Permission", secondary=group_permissions, backref="groups")

    def __unicode__(self):
        return self.name

class Permission(Base):
    __label__ = _('Permission')
    __plural__ = _('Permissions')
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False, label=_('Name'))

    def __unicode__(self):
        return self.name

def populate():
    import random
    session = DBSession()

    for i, name in enumerate(['Admin', 'Read', 'Write']):
        o = Permission()
        o.id = i
        o.name = name
        session.add(o)
    transaction.commit()

    for i, name in enumerate(['Admins', 'Users']):
        o = Group()
        o.id = i
        o.name = name
        o.permissions.append(random.choice(session.query(Permission).all()))
        session.add(o)
    transaction.commit()

    for i, name in enumerate(['John', 'Jack', 'Daniel']):
        o = User()
        o.id = i
        o.name = name
        o.group = random.choice(session.query(Group).all())
        session.add(o)


    for i in range(50):
        article = Article(id=i,
                title='Article %s' % i,
                text='''Heading
=====================

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.

* Morbi id orci augue, porta malesuada mi.
* Proin rhoncus tellus non orci iaculis pretium.
* Praesent aliquet commodo urna, vitae laoreet arcu porttitor ut.
* Nullam sollicitudin blandit risus, eu luctus nisl scelerisque eget.


Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent consectetur
imperdiet porta. Pellentesque habitant morbi tristique senectus et netus et
malesuada fames ac turpis egestas. Proin sollicitudin, mi sit amet blandit
dignissim, lacus ante sagittis est, in congue lectus nulla non urna. Nunc a
justo ut lacus laoreet facilisis. Nullam blandit posuere mauris semper
pellentesque. Sed leo neque, vulputate sed pharetra vel, rhoncus at nisl.
Aenean eget nibh turpis. Quisque semper lacus sodales libero dictum pretium.
Phasellus euismod, odio sit amet vehicula pharetra, nunc diam imperdiet dui,
non malesuada neque erat ac augue. Sed elit ipsum, placerat vitae accumsan
quis, tempor in tellus. Vestibulum tempus consequat libero, sit amet
pellentesque lacus interdum in. Vestibulum in nunc at nulla ultrices laoreet.
''',
            publication_date = datetime.utcnow(),
            user=random.choice(session.query(User).all())
            )
        session.add(article)

    for i in range(100):
        widgets = Widgets(id=i,
                autocomplete=random.choice(['%sanux' % s for s in 'BCDFGHJKLMNP']+['']),
                color = random.choice(["#EEEEEE", "#FFFF88", "#FF7400", "#CDEB8B", "#6BBA70"]),
                slider = random.choice(range(0, 100, 10)),
                )
        session.add(widgets)
    transaction.commit()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        populate()
    except IntegrityError, e:
        DBSession.rollback()
