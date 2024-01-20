
from django.http import Http404
from django_couch import ResourceNotFound

def get_doc_or_404(db, doc_id, **kwargs):
    """
Loads document by id project_id and check field type to have value "project". Otherwise, raise django.http.Http404 exception

::

  def view(request):
      project = django_couch.get_doc_or_404(request.db, project_id, type='project')

"""

    doc = None

    try:
        doc = db[doc_id]
    except ResourceNotFound:
        pass


    if doc is None:
        raise Http404("File not found")

    for key, value in kwargs.items():
        if doc[key] != value:
            raise Http404("File not found")

    return doc
