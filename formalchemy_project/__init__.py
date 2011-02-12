from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from formalchemy_project.models import initialize_sql

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)

    # pyramid_formalchemy's configuration
    config.include('pyramid_formalchemy')
    config.include('fa.jquery')
    config.formalchemy_admin('admin', package='formalchemy_project', view='fa.jquery.pyramid.ModelView')

    return config.make_wsgi_app()


