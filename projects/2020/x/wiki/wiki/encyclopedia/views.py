from django.http import Http404
from django.shortcuts import render
from .util import get_entry
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, title):
    content = get_entry(title)
    if content is not None:
        html_content = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {"title": title, "content": html_content})
    else:
        raise Http404("Entry does not exist")