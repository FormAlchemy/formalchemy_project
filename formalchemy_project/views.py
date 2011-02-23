from formalchemy_project.models import DBSession
from formalchemy_project.models import Article

def my_view(request):
    dbsession = DBSession()
    root = dbsession.query(Article).first()
    return {'root':root, 'project':'formalchemy_project'}
