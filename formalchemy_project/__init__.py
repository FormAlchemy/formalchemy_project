from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from formalchemy_project.models import initialize_sql
import pyramid_formalchemy

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    config = Configurator(settings=settings)

    # formalchemy configuration to enable jquery.ui
    pyramid_formalchemy.include_jquery(config)
    pyramid_formalchemy.configure(config, package='formalchemy_project', use_jquery=True)

    return config.make_wsgi_app()


