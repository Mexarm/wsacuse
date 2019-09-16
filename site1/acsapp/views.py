from django.shortcuts import render, get_object_or_404
from .models import DocImage

from django.http import HttpResponse
from django.contrib.auth.views import login_required


@login_required
def download(request, docid=None):
    print(docid)
    doc = get_object_or_404(DocImage, uuid=docid)
    filename = doc.download()
    with open(filename, 'rb') as handle:
        return HttpResponse(handle.read(), content_type="image/jpeg")
