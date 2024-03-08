from django.http import Http404
from django.shortcuts import render
from .util import get_entry

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_name(request, title):
    content = get_entry(title)
    if content is not None:
         return render(request, "encyclopedia/entry.html", {"title": title, "content": content})
    else:
        raise Http404("Entry does not exist")
     