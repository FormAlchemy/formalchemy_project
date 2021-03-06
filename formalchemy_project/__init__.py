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
    config.include('fa.jquery')
    config.include('fa.extjs')

    # Admin UI (Used for the demo. Not really useful here...)
    config.formalchemy_admin('/extjs', package='formalchemy_project', view='fa.extjs.ModelView')
    config.formalchemy_admin('/admin', package='formalchemy_project', view='fa.jquery.pyramid.ModelView')

    # Article admin UI. Use a custom query_factory to filter by user

    # Here is the interesting part
    def query_factory(request, query, id=None):
        """this query factory use request.matchdict to retrieve user's
        articles. Of course, you can do anything like check that the user found
        in matchdict is the REMOTE_USER"""
        user = request.session_factory.query(models.User).filter_by(name=request.matchdict['user']).one()
        if id:
            return query.filter_by(user=user, id=id).one()
        else:
            return query.filter_by(user=user)

    config.formalchemy_model('/articles/{user}', package='formalchemy_project',
                             model='formalchemy_project.models.Article',
                             query_factory=query_factory,
                             view='fa.jquery.pyramid.ModelView')

    return config.make_wsgi_app()


