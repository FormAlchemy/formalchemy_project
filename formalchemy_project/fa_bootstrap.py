from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from formalchemy_project import models

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    models.initialize_sql(engine)
    config = Configurator(settings=settings)
    config.include('pyramid_tm')
    config.add_translation_dirs('formalchemy_project:locale/')

    # pyramid_formalchemy's configuration
    config.include('pyramid_formalchemy')
    config.include('fa.bootstrap')
    config.include('fa.extjs')

    # Admin UI (Used for the demo. Not really useful here...)
    config.formalchemy_admin('/admin', package='formalchemy_project', view='fa.bootstrap.views.ModelView')

    return config.make_wsgi_app()


